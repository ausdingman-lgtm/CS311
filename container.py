"""
Lab 1: The Typed Script -- TypedContainer starter.

Complete TypedContainer below. See the assignment, Part B,
for the full requirements. Do not rename the class or its methods --
test_container.py imports them by name.
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class TypedContainer(Generic[T]):
    """A strictly-typed key-value container. Keys must always be str."""

    def __init__(self) -> None:
       self._storage: dict[str, T] = {}
       

    def set(self, key: str, value: T) -> None:
        """
        Store `value` under `key`.

        Must raise TypeError immediately if `key` is not a str --
        no silent coercion. See Part A, Question 3, for why.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a str")
        self._storage[key] = value

    def get(self, key: str) -> T:
        """
        Return the value stored under `key`.

        Must raise TypeError immediately if `key` is not a str.
        """
        if not isinstance(key, str):
            raise TypeError("key must be a str")
        return self._storage[key]
    def __contains__(self, key: str) -> bool:
       if not isinstance(key, str):
           raise TypeError("key must be a str")
       return key in self._storage
    def __len__(self) -> int:
        return len(self._storage)
    
