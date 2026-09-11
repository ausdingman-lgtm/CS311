"""
Homework 2: The Playlist Shuffler -- starter.

Complete CircularPlaylist below. See HW2_The_Playlist_Shuffler.md,
Part B, for the full requirements.
"""

from typing import List, Optional


class _SongNode:
    __slots__ = ("name", "next")

    def __init__(self, name: str) -> None:
        self.name = name
        self.next: Optional["_SongNode"] = None


class CircularPlaylist:
    def __init__(self) -> None:
        self._current: Optional[_SongNode] = None  # the "currently playing" node
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def add_song(self, name: str) -> None:
        """Insert `name` at the end of the circle (its next wraps back to the head)."""
        new_node = _SongNode(name)

        if self._current is None:
            # First song points to itself.
            new_node.next = new_node
            self._current = new_node
        else:
            # Find the last node, which points back to the current/head.
            last = self._current
            while last.next is not self._current:
                last = last.next  # type: ignore[assignment]

            new_node.next = self._current
            last.next = new_node

        self._size += 1

    def skip_next(self) -> str:
        """Advance the currently-playing pointer to the next song and return its name."""
        if self._current is None:
            raise IndexError("cannot skip an empty playlist")

        self._current = self._current.next
        return self._current.name  # type: ignore[union-attr]

    def remove_current(self) -> str:
        """
        Remove the currently-playing song, rewire the circle around it,
        advance to the next song, and return the name of the removed song.
        """
        if self._current is None:
            raise IndexError("cannot remove from an empty playlist")

        removed_name = self._current.name

        # One-song playlist.
        if self._size == 1:
            self._current = None
            self._size = 0
            return removed_name

        # Find the node immediately before the current node.
        previous = self._current
        while previous.next is not self._current:
            previous = previous.next  # type: ignore[assignment]

        # Save the next node before removing current.
        next_node = self._current.next

        # Skip over the current node.
        previous.next = next_node

        # Advance currently-playing pointer.
        self._current = next_node

        self._size -= 1

        return removed_name

    def elimination_shuffle(self, k: int) -> List[str]:
        """
        Repeatedly skip k-1 songs and remove the k-th (the Josephus
        pattern from Part A, Question 3), until one song remains.
        Return the removed songs in removal order, with the survivor
        as the final element of the list.
        """
        if k <= 0:
            raise ValueError("k must be positive")

        result: List[str] = []

        while self._size > 1:
            # Skip k-1 songs, then remove the k-th song.
            for _ in range(k - 1):
                self.skip_next()

            result.append(self.remove_current())

        # Add the final survivor.
        if self._current is not None:
            result.append(self._current.name)

        return result
