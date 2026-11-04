"""
Homework 4: The Pruning Gardener -- starter.

Complete delete, count_nodes, and kth_smallest below. TreeNode and
insert are already provided -- do not modify them. See
HW4_The_Pruning_Gardener.md, Part B, for the full requirements.
"""

from typing import Optional


class TreeNode:
    __slots__ = ("key", "left", "right")

    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def insert(root: Optional[TreeNode], key: int) -> TreeNode:
    """Given: standard BST insert. Do not modify."""
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root


def delete(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if root is None:
        return None

    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        # Case 1: No children
        if root.left is None and root.right is None:
            return None

        # Case 2: One child
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left

        # Case 3: Two children — use inorder successor
        successor = root.right
        while successor.left is not None:
            successor = successor.left

        root.key = successor.key
        root.right = delete(root.right, successor.key)

    return root


def count_nodes(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    return 1 + count_nodes(root.left) + count_nodes(root.right)


def kth_smallest(root: Optional[TreeNode], k: int) -> Optional[int]:
    if root is None or k < 1 or k > count_nodes(root):
        return None

    left_count = count_nodes(root.left)

    if k == left_count + 1:
        return root.key
    elif k <= left_count:
        return kth_smallest(root.left, k)
    else:
        return kth_smallest(root.right, k - left_count - 1)