from ass3.model.State import State
from ass3.util.StateGenerator import generate_moves


def alpha_beta_pruning(n, taken_tokens, max_depth, is_max_player):
    nodes_visited = 0
    eval_nodes = 0
    max_level = 0
    successors = 0
    number_of_nodes = 0

    def dfs(root: State, alpha: float, beta: float, level: int):
        nonlocal nodes_visited, eval_nodes, max_level, successors, number_of_nodes
        root.moves = generate_moves(root)
        nodes_visited += 1
        max_level = max(max_level, level)
        if (root.max_depth != 0 and level == root.max_depth) or len(root.moves) == 0:
            eval_nodes += 1
            return root.heuristic_value(), root

        value = float("-inf") if root.is_max_player else float("inf")
        best_move = None
        non_pruned_successors = 0

        for move in root.moves:
            heuristic_val, child_move = dfs(move, alpha, beta, level + 1)
            if root.is_max_player:
                if value < heuristic_val:
                    value = heuristic_val
                    best_move = move
                elif value == heuristic_val and best_move.taken_tokens[-1] > move.taken_tokens[-1]:
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value > heuristic_val:
                    value = heuristic_val
                    best_move = move
                elif value == heuristic_val and best_move.taken_tokens[-1] > move.taken_tokens[-1]:
                    best_move = move
                beta = min(beta, value)
            if beta <= alpha:
                return value, None
            if child_move:
                non_pruned_successors += 1

        if non_pruned_successors > 0:
            number_of_nodes += 1
            successors += non_pruned_successors

        return value, best_move

    initial_state = State(n, taken_tokens, max_depth, is_max_player)
    score, next_move = dfs(initial_state, float("-inf"), float("inf"), 0)
    return score, next_move, nodes_visited, eval_nodes, max_level, successors / number_of_nodes
