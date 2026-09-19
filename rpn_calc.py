"""
Lab 5: The Postfix Calculator -- starter + verification (single file).

Complete Stack, evaluate_postfix, and is_balanced below. See
Lab_05_The_Postfix_Calculator.md, Part B, for the full requirements.
Do not modify main() or anything below the "VERIFICATION SUITE" line.

Run: python rpn_calc.py
"""

import base64
import hashlib
import sys
from typing import Generic, List, TypeVar

T = TypeVar("T")

ASSIGNMENT_ID = "LAB05"


class Stack(Generic[T]):
    """A LIFO stack. Callers may only use push/pop/peek/is_empty."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)


    def pop(self) -> T:
        """Remove and return the top item. Raise IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        """Return (without removing) the top item. Raise IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0


def evaluate_postfix(expression: str) -> float:
    """
    Evaluate a space-separated postfix (RPN) expression, e.g. "6 2 3 + - 4 *".
    Supports + - * /. Raise ValueError (with a descriptive message) on
    malformed input -- too many operators, division by zero, etc.
    """
    stack: Stack[float] = Stack()

    tokens = expression.split()

    if not tokens:
        raise ValueError("empty expression")

    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            if stack.is_empty():
                raise ValueError("not enough operands for operator")

            right = stack.pop()

            if stack.is_empty():
                raise ValueError("not enough operands for operator")

            left = stack.pop()

            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            else:
                if right == 0:
                    raise ValueError("division by zero")
                result = left / right

            stack.push(result)

        else:
            try:
                number = float(token)
            except ValueError:
                raise ValueError(f"invalid token: {token}")

            stack.push(number)

    if stack.is_empty():
        raise ValueError("malformed expression")

    if stack.peek() is not None:
        result = stack.pop()

    if not stack.is_empty():
        raise ValueError("too many operands")

    return result


def is_balanced(expression: str) -> bool:
    """
    Return True if all of (), [], {} in `expression` are correctly
    matched and nested. Must reuse the Stack class above. Handles
    mismatched-type closes, unmatched opens, and unmatched closes by
    returning False -- never raise.
    """
    stack: Stack[str] = Stack()

    opening = "([{"
    matching = {
        ")": "(",
        "]": "[",
        "}": "{"
    }

    for char in expression:
        if char in opening:
            stack.push(char)

        elif char in matching:
            if stack.is_empty():
                return False

            if stack.pop() != matching[char]:
                return False

    return stack.is_empty()


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

    print("Testing Stack...\n")
    s: Stack = Stack()
    check("new stack is empty", s.is_empty(), failures)
    s.push(1)
    s.push(2)
    check("peek returns top without removing", s.peek() == 2 and not s.is_empty(), failures)
    check("pop returns and removes top (LIFO order)", s.pop() == 2, failures)
    check("pop again returns first-pushed item", s.pop() == 1, failures)
    check("stack empty again after two pops", s.is_empty(), failures)
    try:
        s.pop()
        check("pop on empty stack raises", False, failures)
    except IndexError:
        check("pop on empty stack raises IndexError", True, failures)

    print("\nTesting evaluate_postfix...\n")
    postfix_cases = [
        ("6 2 3 + - 4 *", 4.0),    # from Part A, Question 1: (6 - (2+3)) * 4 = 1 * 4 = 4
        ("2 3 +", 5.0),
        ("5 1 2 + 4 * + 3 -", 14.0),
        ("10 2 /", 5.0),
        ("4 2 -", 2.0),
        ("2 3 -", -1.0),           # non-commutative: order matters
        ("10 2 3 - /", -10.0),     # 2 3 - = -1, then 10 / -1 = -10.0
    ]

    for expr, expected in postfix_cases:
        try:
            result = evaluate_postfix(expr)
            check(f"evaluate_postfix('{expr}') == {expected}", abs(result - expected) < 1e-9, failures)
        except Exception as e:
            check(f"evaluate_postfix('{expr}') == {expected} (raised {e!r})", False, failures)

    malformed_cases = ["1 +", "1 2 3 +", "5 0 /"]
    for expr in malformed_cases:
        try:
            evaluate_postfix(expr)
            check(f"evaluate_postfix('{expr}') raises ValueError on malformed input", False, failures)
        except ValueError:
            check(f"evaluate_postfix('{expr}') raises ValueError on malformed input", True, failures)
        except Exception as e:
            check(f"evaluate_postfix('{expr}') raises ValueError, not {type(e).__name__}", False, failures)

    print("\nTesting is_balanced...\n")
    balanced_cases = [
        ("()", True), ("[]", True), ("{}", True),
        ("({[]})", True), ("(a[b]{c})", True), ("", True),
        ("(]", False), ("(((", False), (")))", False),
        ("([)]", False), ("{[()]}", True), ("{[(])}", False),
        ("(()", False), ("())", False),
    ]
    for expr, expected in balanced_cases:
        try:
            result = is_balanced(expr)
            check(f"is_balanced('{expr}') == {expected}", result == expected, failures)
        except Exception as e:
            check(f"is_balanced('{expr}') == {expected} (raised {e!r} instead of returning)", False, failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
