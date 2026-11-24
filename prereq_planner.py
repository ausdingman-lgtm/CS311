
"""
Homework 6: The Prerequisite Planner -- starter.

Complete has_cycle and topological_sort below. See
Homework 6 The Prerequisite Planner.md, Part B, for the full requirements.
"""

from typing import Dict, List, Optional


def has_cycle(graph: Dict[str, List[str]]) -> bool:
    """
    Recursive DFS. Track both a permanent "visited" set and a
    temporary "on the current recursion path" set to detect back
    edges (Part A, Question 4). Must work across disconnected
    components.
    """
    visited = set()
    on_path = set()

    def dfs(node):
        visited.add(node)
        on_path.add(node)

        for neighbor in graph.get(node, []):
            if neighbor in on_path:
                return True

            if neighbor not in visited:
                if dfs(neighbor):
                    return True

        on_path.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True

    return False


def topological_sort(graph: Dict[str, List[str]]) -> Optional[List[str]]:
    """
    Return a valid topological order via DFS finish-time ordering
    (Part A, Questions 2-3), or None if the graph contains a cycle.
    """
    visited = set()
    on_path = set()
    result = []

    def dfs(node):
        visited.add(node)
        on_path.add(node)

        for neighbor in graph.get(node, []):
            if neighbor in on_path:
                return False

            if neighbor not in visited:
                if not dfs(neighbor):
                    return False

        on_path.remove(node)
        result.append(node)
        return True

    for node in graph:
        if node not in visited:
            if not dfs(node):
                return None

    result.reverse()
    return result
