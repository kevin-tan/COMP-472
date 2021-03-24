from ass2.model.Node import *
from ass2.util.StateGenerator import next_node
import heapq


def a_star_search_h1(initial_state, goal_state):
    return proper_a_star(Node(initial_state, 0, heuristic=heuristic_h1), set(), goal_state, heuristic_h1)


def a_star_search_h2(initial_state, goal_state):
    return proper_a_star(Node(initial_state, 0, heuristic=heuristic_h2), set(), goal_state, heuristic_h2)


def proper_a_star(root, visited, goal_state, heuristic):
    heap = [root]
    search_path = []
    while len(heap) > 0:
        current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)
        state = current_node.state
        search_path.append(state)

        if current_node.is_goal_state(goal_state):
            return current_node, search_path

        row_len = len(state)
        col_len = len(state[0])
        for row in range(0, row_len):
            for col in range(0, col_len):
                if col + 1 < col_len:
                    node = next_node(current_node, row, col, row, col + 1, current_node.depth + 1, heuristic)
                    if node not in visited:
                        heapq.heappush(heap, node)
                if row + 1 < row_len:
                    node = next_node(current_node, row, col, row + 1, col, current_node.depth + 1, heuristic)
                    if node not in visited:
                        heapq.heappush(heap, node)
    return None, search_path


def heuristic_h1(current_node, p1, p2):
    state = current_node.state
    estimate = current_node.depth
    n = len(state)
    for row in range(0, n):
        for col in range(0, len(state[row])):
            v1 = state[row][col] - 1
            correct_x_v1 = v1 / n
            correct_y_v1 = v1 % n
            estimate += abs(correct_x_v1 - row) + abs(correct_y_v1 - col)
    return estimate

# After swapping calculating the estimate cost of the next resulting swap
def heuristic_h1_attempt_1(current_node, p1, p2):
    def calculate_estimate(value, current_position, size):
        correct_x = value / size
        correct_y = value % size
        return abs(correct_x - current_position[0]) + abs(correct_y - current_position[1])

    def find_future_swap_position(s, p, size):
        value_p = s[p[0]][p[1]] - 1
        target_p = (int(value_p / size), value_p % size)
        x = target_p[0]
        y = target_p[1]
        if p[1] < target_p[1]:
            y -= 1
        elif p[1] > target_p[1]:
            y += 1

        if p[0] < target_p[0]:
            x -= 1
        elif p[0] > target_p[0]:
            x += 1
        return s[target_p[0]][target_p[1]], (x, y)

    state = current_node.state
    n = len(state)
    estimate = current_node.depth + base_heuristic(current_node, p1, p2)
    # p1 target
    p1_target = find_future_swap_position(state, p1, n)
    estimate += calculate_estimate(p1_target[0], p1_target[1], n)
    # p2 target
    p2_target = find_future_swap_position(state, p2, n)
    estimate += calculate_estimate(p2_target[0], p2_target[1], n)
    return estimate


# We are only concerned about the cost associated with the resulting swap (i.e. did it make the numbers further)
def heuristic_h2(current_node, p1, p2):
    return current_node.depth + base_heuristic(current_node, p1, p2)


def base_heuristic(current_node, p1, p2):
    state = current_node.state
    n = len(state)
    estimate = 0
    v1 = state[p1[0]][p1[1]] - 1
    correct_x_v1 = v1 / n
    correct_y_v1 = v1 % n
    estimate += abs(correct_x_v1 - p1[0]) + abs(correct_y_v1 - p1[1])
    v2 = state[p2[0]][p2[1]] - 1
    correct_x_v2 = v2 / n
    correct_y_v2 = v2 % n
    estimate += abs(correct_x_v2 - p2[0]) + abs(correct_y_v2 - p2[1])
    return estimate
