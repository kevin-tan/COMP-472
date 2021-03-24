from datetime import datetime

from ass2.model.Node import *
from ass2.util.StateGenerator import generate_next_state


def depth_first_search(initial_state, goal_state):
    return proper_dfs(Node(initial_state, 0), set(), goal_state)


def proper_dfs(root, visited, goal_state):
    time_start = datetime.now()
    stack = [root]
    search_path = []
    while len(stack) > 0 and (datetime.now() - time_start).total_seconds() < 60:
        current_node = stack.pop()
        visited.add(current_node)
        search_path.append(current_node)

        if current_node.is_goal_state(goal_state):
            return current_node, search_path

        # Generate next state
        next_node = generate_next_state(current_node, visited)
        if next_node is not None:
            stack.append(current_node)
            stack.append(next_node)

    return None, search_path
