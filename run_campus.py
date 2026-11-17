"""
Lab 12: USI Campus Connector -- starter + verification (single file).

Complete build_graph, has_path, and bfs_shortest_path below. Do not
modify anything below the "VERIFICATION SUITE" line.

Run: python run_campus.py
"""

import base64
import hashlib
import sys
from collections import deque
from typing import Dict, List, Optional, Set

ASSIGNMENT_ID = "LAB12"



def build_graph(connector_groups: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Turn {connector group: [building list]} into an adjacency list: every pair of
    buildings in the same connector group is connected by an edge (undirected).
    """
    graph = {}

    for buildings in connector_groups.values():
        for building in buildings:
            if building not in graph:
                graph[building] = []

            for other in buildings:
                if other != building and other not in graph[building]:
                    graph[building].append(other)

    return graph


def has_path(graph: Dict[str, List[str]], start: str, target: str, visited: Optional[Set[str]] = None) -> bool:
    """
    Recursive DFS sanity-check: True if `start` and `target` are
    connected at all (not necessarily the shortest way).
    Must handle start == target, and a fully exhausted search.
    """
    if start == target:
        return True

    if visited is None:
        visited = set()

    visited.add(start)

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            if has_path(graph, neighbor, target, visited):
                return True

    return False


def bfs_shortest_path(graph: Dict[str, List[str]], start: str, target: str) -> Optional[List[str]]:
    """
    Iterative (BFS is naturally level-by-level -- explain in a comment
    why recursion isn't the natural fit here). Use collections.deque.
    Return the ordered list of buildings forming the shortest chain from
    `start` to `target`, or None if no path exists.
    """
    # BFS processes nodes queue-first, level by level, rather than
    # diving depth-first along one branch -- that's an inherently
    # iterative "expand the frontier" process, not a "solve a smaller
    # version of the same problem" one, so a loop over an explicit
    # queue is the natural fit here rather than recursion.

    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == target:
            return path

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None


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

    # From Part A, Question 2
    connector_groups = {
        "Link 1": ["Rice Library", "University Center"],
        "Link 2": ["University Center", "Science Center"],
        "Link 3": ["Science Center", "Orr Center"],
        "Link 4": ["Rice Library", "Liberal Arts Center"],
    }

    print("Testing build_graph...\n")
    graph = build_graph(connector_groups)
    check("Rice Library-University Center edge exists both directions", "University Center" in graph.get("Rice Library", []) and "Rice Library" in graph.get("University Center", []), failures)
    check("University Center-Science Center edge exists both directions", "Science Center" in graph.get("University Center", []) and "University Center" in graph.get("Science Center", []), failures)
    check("Science Center-Orr Center edge exists both directions", "Orr Center" in graph.get("Science Center", []) and "Science Center" in graph.get("Orr Center", []), failures)
    check("Rice Library-Liberal Arts Center edge exists both directions", "Liberal Arts Center" in graph.get("Rice Library", []) and "Rice Library" in graph.get("Liberal Arts Center", []), failures)
    check("Rice Library and Orr Center are NOT directly connected (no shared connector group)", "Orr Center" not in graph.get("Rice Library", []), failures)

    if failures:
        print(f"\n{len(failures)} build_graph check(s) failed -- fix these first. No token issued.")
        return 1

    print("\nTesting has_path...\n")
    check("has_path(Rice Library, Orr Center) is True (connected via University Center, Science Center)", has_path(graph, "Rice Library", "Orr Center") is True, failures)
    check("has_path(Rice Library, Rice Library) is True (start == target)", has_path(graph, "Rice Library", "Rice Library") is True, failures)
    check("has_path to a nonexistent building is False", has_path(graph, "Rice Library", "Missing Building") is False, failures)

    isolated_graph = build_graph({"Isolated building": ["Performance Center"]})
    full_graph = {**graph, **isolated_graph}
    check("has_path between disconnected components is False", has_path(full_graph, "Rice Library", "Performance Center") is False, failures)

    print("\nTesting bfs_shortest_path...\n")
    path = bfs_shortest_path(graph, "Rice Library", "Orr Center")
    check("bfs_shortest_path(Rice Library, Orr Center) == [Rice Library, University Center, Science Center, Orr Center]", path == ["Rice Library", "University Center", "Science Center", "Orr Center"], failures)
    check("bfs_shortest_path(Rice Library, Rice Library) == [Rice Library]", bfs_shortest_path(graph, "Rice Library", "Rice Library") == ["Rice Library"], failures)
    check("bfs_shortest_path returns None when no path exists", bfs_shortest_path(full_graph, "Rice Library", "Performance Center") is None, failures)

    # A slightly bigger graph to confirm true shortest-path behavior (not just any path)
    bigger = {
        "Link X": ["Rice Library", "University Center", "Science Center"],
        "Link Y": ["Science Center", "Orr Center"],
        "Link Z": ["Rice Library", "Orr Center"],  # shortcut: Rice Library–Orr Center directly, should beat A-B-C-D
    }
    bigger_graph = build_graph(bigger)
    shortest = bfs_shortest_path(bigger_graph, "Rice Library", "Orr Center")
    check("bfs_shortest_path finds the true shortest chain, not just any chain", shortest == ["Rice Library", "Orr Center"], failures)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed. No token issued.")
        return 1

    print_success_banner(ASSIGNMENT_ID)
    return 0


if __name__ == "__main__":
    sys.exit(main())
