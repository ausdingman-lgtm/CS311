"""
Homework 1: The Sorting Showdown -- starter.

Complete the two functions below. See
HW1_The_Sorting_Showdown.md, Part B, for the full requirements.
"""

from typing import List


def insertion_sort(data: List[int]) -> List[int]:
    """

    Time complexity:
        Best: O(n)
        Average: O(n^2)
        Worst: O(n^2)
    """
    result = data.copy()

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def selection_sort(data: List[int]) -> List[int]:
    """

    Time complexity:
        Best: O(n^2)
        Average: O(n^2)
        Worst: O(n^2)
    """
    result = data.copy()

    for i in range(len(result)):
        min_index = i

        for j in range(i + 1, len(result)):
            if result[j] < result[min_index]:
                min_index = j

        if min_index != i:
            result[i], result[min_index] = result[min_index], result[i]

    return result