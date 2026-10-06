"""
Lab 7: The Collision Resolver -- completed.
"""

from typing import Generic, Hashable, List, Optional, Tuple, TypeVar


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

_TOMBSTONE = object()


class _ChainNode(Generic[K, V]):
    __slots__ = ("key", "value", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.next: Optional["_ChainNode[K, V]"] = None


class ChainedHashMap(Generic[K, V]):
    """Separate chaining: each bucket is a linked list of (key, value)."""

    def __init__(self, initial_size: int = 16) -> None:
        self._buckets: List[Optional[_ChainNode[K, V]]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Insert, or update in place if `key` already exists.
        Resize (double + rehash) once load factor > 0.75.
        """
        index = hash(key) % len(self._buckets)

        # Check whether key already exists
        current = self._buckets[index]
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # Insert new node at front of chain
        new_node = _ChainNode(key, value)
        new_node.next = self._buckets[index]
        self._buckets[index] = new_node
        self._count += 1

        # Resize if load factor exceeds 0.75
        if self._count / len(self._buckets) > 0.75:
            old_buckets = self._buckets
            self._buckets = [None] * (len(old_buckets) * 2)

            for node in old_buckets:
                current = node
                while current is not None:
                    next_node = current.next

                    index = hash(current.key) % len(self._buckets)
                    current.next = self._buckets[index]
                    self._buckets[index] = current

                    current = next_node

    def get(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""
        index = hash(key) % len(self._buckets)

        current = self._buckets[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(key)

    def delete(self, key: K) -> None:
        """Remove `key`. Raise KeyError if missing."""
        index = hash(key) % len(self._buckets)

        current = self._buckets[index]
        previous = None

        while current is not None:
            if current.key == key:
                if previous is None:
                    self._buckets[index] = current.next
                else:
                    previous.next = current.next

                self._count -= 1
                return

            previous = current
            current = current.next

        raise KeyError(key)


class LinearProbingHashMap(Generic[K, V]):
    """Open addressing with linear probing and tombstone deletion."""

    def __init__(self, initial_size: int = 16) -> None:
        self._keys: List[object] = [None] * initial_size
        self._values: List[Optional[V]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Resize (double + rehash) once load factor > 0.7."""

        # Resize before insertion if necessary
        if (self._count + 1) / len(self._keys) > 0.7:
            self._resize(len(self._keys) * 2)

        index = hash(key) % len(self._keys)
        first_tombstone = None

        for _ in range(len(self._keys)):
            current_key = self._keys[index]

            # Empty slot
            if current_key is None:
                if first_tombstone is not None:
                    index = first_tombstone

                self._keys[index] = key
                self._values[index] = value
                self._count += 1
                return

            # Tombstone
            if current_key is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = index

            # Existing key
            elif current_key == key:
                self._values[index] = value
                return

            index = (index + 1) % len(self._keys)

        # Should not normally happen because of resizing
        if first_tombstone is not None:
            self._keys[first_tombstone] = key
            self._values[first_tombstone] = value
            self._count += 1
            return

        raise RuntimeError("Hash table is full")

    def search(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""

        index = hash(key) % len(self._keys)

        for _ in range(len(self._keys)):
            current_key = self._keys[index]

            if current_key is None:
                raise KeyError(key)

            if current_key is not _TOMBSTONE and current_key == key:
                return self._values[index]  # type: ignore

            index = (index + 1) % len(self._keys)

        raise KeyError(key)

    def delete(self, key: K) -> None:
        """Remove `key` using a tombstone."""

        index = hash(key) % len(self._keys)

        for _ in range(len(self._keys)):
            current_key = self._keys[index]

            if current_key is None:
                raise KeyError(key)

            if current_key is not _TOMBSTONE and current_key == key:
                self._keys[index] = _TOMBSTONE
                self._values[index] = None
                self._count -= 1
                return

            index = (index + 1) % len(self._keys)

        raise KeyError(key)

    def _resize(self, new_size: int) -> None:
        old_keys = self._keys
        old_values = self._values

        self._keys = [None] * new_size
        self._values = [None] * new_size
        self._count = 0

        for i, key in enumerate(old_keys):
            if key is not None and key is not _TOMBSTONE:
                self.insert(key, old_values[i])  # type: ignore


class QuadraticProbingHashMap(Generic[K, V]):
    """
    Open addressing with quadratic probing and tombstone deletion.
    """

    def __init__(self, initial_size: int = 17) -> None:
        self._keys: List[object] = [None] * initial_size
        self._values: List[Optional[V]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Resize (grow + rehash) once load factor > 0.7."""

        # Resize BEFORE probing if insertion would exceed 0.7
        if (self._count + 1) / len(self._keys) > 0.7:
            self._resize(self._next_prime(len(self._keys) * 2))

        start = hash(key) % len(self._keys)
        first_tombstone = None

        for i in range(len(self._keys)):
            index = (start + i * i) % len(self._keys)
            current_key = self._keys[index]

            # Empty slot
            if current_key is None:
                if first_tombstone is not None:
                    index = first_tombstone

                self._keys[index] = key
                self._values[index] = value
                self._count += 1
                return

            # Tombstone
            if current_key is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = index

            # Existing key
            elif current_key == key:
                self._values[index] = value
                return

        # Use a tombstone if one was found
        if first_tombstone is not None:
            self._keys[first_tombstone] = key
            self._values[first_tombstone] = value
            self._count += 1
            return

        # Safety fallback
        self._resize(self._next_prime(len(self._keys) * 2))
        self.insert(key, value)

    def search(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""

        start = hash(key) % len(self._keys)

        for i in range(len(self._keys)):
            index = (start + i * i) % len(self._keys)
            current_key = self._keys[index]

            if current_key is None:
                raise KeyError(key)

            if current_key is not _TOMBSTONE and current_key == key:
                return self._values[index]  # type: ignore

        raise KeyError(key)

    def delete(self, key: K) -> None:
        """Remove `key` using a tombstone. Raise KeyError if missing."""

        start = hash(key) % len(self._keys)

        for i in range(len(self._keys)):
            index = (start + i * i) % len(self._keys)
            current_key = self._keys[index]

            if current_key is None:
                raise KeyError(key)

            if current_key is not _TOMBSTONE and current_key == key:
                self._keys[index] = _TOMBSTONE
                self._values[index] = None
                self._count -= 1
                return

        raise KeyError(key)

    def _resize(self, new_size: int) -> None:
        old_keys = self._keys
        old_values = self._values

        self._keys = [None] * new_size
        self._values = [None] * new_size
        self._count = 0

        for i, key in enumerate(old_keys):
            if key is not None and key is not _TOMBSTONE:
                self.insert(key, old_values[i])  # type: ignore

    @staticmethod
    def _is_prime(n: int) -> bool:
        if n < 2:
            return False

        if n == 2:
            return True

        if n % 2 == 0:
            return False

        divisor = 3
        while divisor * divisor <= n:
            if n % divisor == 0:
                return False
            divisor += 2

        return True

    @classmethod
    def _next_prime(cls, n: int) -> int:
        while not cls._is_prime(n):
            n += 1
        return n