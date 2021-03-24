from datetime import datetime

from ass2.model.Node import *
from ass2.util.StateGenerator import generate_next_state


def iterative_deepening(initial_state, goal_state):
    return proper_idfs(Node(initial_state, 0), goal_state)


def proper_idfs(root, goal_state):
    time_start = datetime.now()
    attempts_search_path = []
    level_limit = 1
    while (datetime.now() - time_start).total_seconds() <= 60 or len(goal_state) > 3:
        stack = [root]
        search_path = []
        visited = set()
        while len(stack) > 0 and (datetime.now() - time_start).total_seconds() < 60:
            current_node = stack.pop()
            visited.add(current_node)
            search_path.append(current_node)

            if current_node.is_goal_state(goal_state):
                return current_node, attempts_search_path

            # Generate next state
            if current_node.depth < level_limit:
                next_node = generate_next_state(current_node, visited)
                if next_node is not None:
                    stack.append(current_node)
                    stack.append(next_node)

        attempts_search_path.append(search_path)
        level_limit += 1

    return None, attempts_search_path
