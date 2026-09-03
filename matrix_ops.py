"""
Lab 3: The Row-Major Detective -- starter.

Complete the two functions below. See
Lab_03_The_Row_Major_Detective.md, Part B, for the full requirements.
"""

from typing import List


def transpose_inplace(matrix: List[List[float]]) -> None:
    """
    Transpose a SQUARE matrix in place (no new matrix allocated).
    Mutates `matrix` directly; returns None.
    """
    n = len(matrix)

    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

def transpose_blocked(matrix: List[List[float]], block_size: int) -> List[List[float]]:
    """
    Transpose a (possibly non-square) matrix using a blocked/tiled
    access pattern for cache locality, returning a NEW matrix.
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    result = [[0.0] * rows for _ in range(cols)]

    for i in range(0, rows, block_size):
        for j in range(0, cols, block_size):
            i_end = min(i + block_size, rows)
            j_end = min(j + block_size, cols)

            for x in range(i, i_end):
                row = matrix[x]
                for y in range(j, j_end):
                    result[y][x] = row[y]

    return result