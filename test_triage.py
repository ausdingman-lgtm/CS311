"""
Lab 10: The Priority Triage -- starter + verification (single file).

Complete insert, _sift_up, _sift_down, and extract_min below. Do not
modify anything below the "VERIFICATION SUITE" line.

Run: python test_triage.py
"""

import base64
import hashlib
import random
import sys
from typing import List

ASSIGNMENT_ID = "LAB10"


class MinHeap:
    """A binary min-heap backed by a flat Python list. Lower priority number = more critical."""

    def __init__(self) -> None:
        self._data: List[float] = []

    def __len__(self) -> int:
        return len(self._data)

    def insert(self, value: float) -> None:
        """Append `value`, then call _sift_up to restore the heap property."""
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def _sift_up(self, index: int) -> None:
        """
        Recursive. Perform at most one swap, then recurse toward the
        correct resting position. Do not use a while loop.
        """
        if index == 0:
            return

        parent = (index - 1) // 2

        if self._data[index] < self._data[parent]:
            self._data[index], self._data[parent] = (
                self._data[parent],
                self._data[index],
            )
            self._sift_up(parent)

    def _sift_down(self, index: int) -> None:
        """
        Recursive. Perform at most one swap, then recurse toward the
        correct resting position. Do not use a while loop.
        """
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        if left < len(self._data) and self._data[left] < self._data[smallest]:
            smallest = left

        if right < len(self._data) and self._data[right] < self._data[smallest]:
            smallest = right

        if smallest != index:
            self._data[index], self._data[smallest] = (
                self._data[smallest],
                self._data[index],
            )
            self._sift_down(smallest)

    def extract_min(self) -> float:
        """
        Remove and return the smallest (highest-priority) value.
        Move the last element to the root and call _sift_down.
        Correctly handle a heap with 0 or 1 elements.
        """
        if not self._data:
            raise IndexError("extract_min from empty heap")

        minimum = self._data[0]
        last = self._data.pop()

        if self._data:
            self._data[0] = last
            self._sift_down(0)

        return minimum


# ============================== VERIFICATION SUITE ==============================
# Do not edit below this line.


def get_student_id() -> str:
    """Prompt for the student's USI username; baked into the Success Token
    so a copied/shared token decodes to someone else's name, not yours."""
    student_id = input("Enter your USI username (e.g. cwill): ").strip()
    while not student_id:
        student_id = input("Username cannot be blank. Enter your USI username: ").strip()
    return student_id


def generate_token(assignment_id: str, student_id: str) -> str:
    digest = hashlib.sha256(f"CS311-{assignment_id}-{student_id}-VERIFIED".encode()).hexdigest()[:16]
    raw = f"CS311|{assignment_id}|{student_id}|PASS|{digest}"
    return base64.b64encode(raw.encode()).decode()


def print_success_banner(assignment_id: str) -> None:
    student_id = get_student_id()
    token = generate_token(assignment_id, student_id)
    print("\n" + "=" * 60)
    print(f"  ALL CHECKS PASSED -- {assignment_id}")
    print(f"  STUDENT: {student_id}")
    print("  SUCCESS TOKEN (paste this into Blackboard):")
    print(f"  {token}")
    print("=" * 60 + "\n")


def check(label: str, condition: bool, failures: list) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if not condition:
        failures.append(label)


def is_heap_property(data: List[float]) -> bool:
    for i in range(len(data)):
        left, right = 2 * i + 1, 2 * i + 2
        if left < len(data) and data[left] < data[i]:
            return False
        if right < len(data) and data[right] < data[i]:
            return False
    return True


def main() -> int:
    failures: list = []

    print("Testing against the Part A, Q3 sequence: 5, 3, 8, 1, 9, 2...\n")
    heap = MinHeap()
    for v in [5, 3, 8, 1, 9, 2]:
        heap.insert(v)
        check(f"heap property holds after inserting {v}", is_heap_property(heap._data), failures)
    check("heap has 6 elements after 6 inserts", len(heap) == 6, failures)

    extracted = []
    while len(heap) > 0:
        m = heap.extract_min()
        extracted.append(m)
        check(f"heap property holds after extracting {m}", is_heap_property(heap._data), failures)
    check("extract_min pulls values out in fully sorted order", extracted == sorted([5, 3, 8, 1, 9, 2]), failures)

    print("\nTesting edge cases...\n")
    empty = MinHeap()
    try:
        empty.extract_min()
        check("extract_min on empty heap raises", False, failures)
    except (IndexError, ValueError):
        check("extract_min on empty heap raises IndexError/ValueError", True, failures)

    single = MinHeap()
    single.insert(42)
    check("extract_min on single-element heap returns that element", single.extract_min() == 42, failures)
    check("heap is empty after extracting its only element", len(single) == 0, failures)

    print("\nRandomized stress test (500 random priority values)...\n")
    rng = random.Random(311)
    values = [rng.randint(0, 100_000) for _ in range(500)]
    stress_heap = MinHeap()
    for v in values:
        stress_heap.insert(v)
    stress_extracted = [stress_heap.extract_min() for _ in range(len(values))]
    check("500-value stress test: extract_min order matches sorted order", stress_extracted == sorted(values), failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
