"""
Lab 8: The Tree Walkers -- starter + verification (single file).

Complete search, inorder, preorder, postorder, and to_json below. The
TreeNode class and BST-building insert() are already provided -- do
not modify them, or anything below the "VERIFICATION SUITE" line.

Run: python serialize_tree.py
"""

import base64
import hashlib
import json
import sys
from typing import Any, Dict, List, Optional

ASSIGNMENT_ID = "LAB08"


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


def search(root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
    """
    Recursively find and return the TreeNode containing `target`, or
    None if absent. Must exploit the BST property -- only recurse into
    the one subtree that could possibly contain `target`.
    """
    if root is None:
        return None

    if root.key == target:
        return root
    elif target < root.key:
        return search(root.left, target)
    else:
        return search(root.right, target)


def inorder(root: Optional[TreeNode]) -> List[int]:
    """Return keys in inorder (left, root, right) order."""
    if root is None:
        return []

    return inorder(root.left) + [root.key] + inorder(root.right)


def preorder(root: Optional[TreeNode]) -> List[int]:
    """Return keys in preorder (root, left, right) order."""
    if root is None:
        return []

    return [root.key] + preorder(root.left) + preorder(root.right)


def postorder(root: Optional[TreeNode]) -> List[int]:
    """Return keys in postorder (left, right, root) order."""
    if root is None:
        return []

    return postorder(root.left) + postorder(root.right) + [root.key]


def to_json(root: Optional[TreeNode]) -> Optional[Dict[str, Any]]:
    """Recursively build {"key": ..., "left": <subtree or null>, "right": <subtree or null>}."""
    if root is None:
        return None

    return {
        "key": root.key,
        "left": to_json(root.left),
        "right": to_json(root.right)
    }


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


def main() -> int:
    failures: list = []

    root = None
    for key in [50, 25, 75, 10, 30, 60, 80, 5]:  # from Part A, Question 2
        root = insert(root, key)

    print("Testing search...\n")
    check("search finds an existing key (30)", search(root, 30) is not None and search(root, 30).key == 30, failures)
    check("search returns None for an absent key (99)", search(root, 99) is None, failures)
    check("search on empty tree returns None", search(None, 5) is None, failures)

    print("\nTesting traversals against the Part A, Q2 tree...\n")
    check("inorder matches sorted order", inorder(root) == [5, 10, 25, 30, 50, 60, 75, 80], failures)
    check("preorder matches root-first order", preorder(root) == [50, 25, 10, 5, 30, 75, 60, 80], failures)
    check("postorder matches children-before-root order", postorder(root) == [5, 10, 30, 25, 60, 80, 75, 50], failures)

    check("inorder/preorder/postorder on empty tree all return []", inorder(None) == [] and preorder(None) == [] and postorder(None) == [], failures)

    print("\nTesting to_json...\n")
    small_root = None
    for key in [2, 1, 3]:
        small_root = insert(small_root, key)
    expected = {"key": 2, "left": {"key": 1, "left": None, "right": None}, "right": {"key": 3, "left": None, "right": None}}
    check("to_json produces the correct nested structure", to_json(small_root) == expected, failures)
    check("to_json on empty tree returns None", to_json(None) is None, failures)

    try:
        json.dumps(to_json(root), indent=2)
        check("to_json output is JSON-serializable", True, failures)
    except (TypeError, ValueError):
        check("to_json output is JSON-serializable", False, failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print(json.dumps(to_json(root), indent=2))
    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
