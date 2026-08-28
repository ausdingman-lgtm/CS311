"""
Lab 2: The Complexity Profiler -- starter.

Complete the three functions below. See the assignment,
Part B, for the full requirements. Do not use sorted(), list.sort(), or
the `in` operator inside these implementations -- hand-roll the logic.
"""

from typing import List


def linear_search(data: List[int], target: int) -> int:
    """
    Return the index of `target` in `data`, or -1 if absent.
    Time complexity:
    Best case: O(1)
    Average case: O(n)
    Worst case: O(n)
    """
    for i in range(len(data)):
        if data[i] == target:
            return i

    return -1


def binary_search(data: List[int], target: int) -> int:
    """
    Return the index of `target` in a SORTED `data`, or -1 if absent.
    Must be iterative, not recursive.
    Time complexity:
    Best case: O(1)
    Average case: O(log n)
    Worst case: O(log n)
    """
    left = 0
    right = len(data) - 1

    while left <= right:
        middle = (left + right) // 2

        if data[middle] == target:
            return middle
        elif data[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1



def bubble_sort(data: List[int]) -> List[int]:
    """
    Return a new list containing `data`'s elements in ascending order.
    Must not mutate the input list.
      Time complexity:
    Best case: O(n)
    Average case: O(n²)
    Worst case: O(n²)
    """
    result = data[:]
    n = len(result)

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        # Stop early if the list is already sorted
        if not swapped:
            break

    return result
