from ass3.model.State import State
from copy import deepcopy


# Generate a resulting state for the next player based on what the current player has taken as a token
def generate_moves(root: State):
    next_moves = []
    last_move = root.taken_tokens[-1] if len(root.taken_tokens) > 0 else None

    if last_move is None:
        length = root.n / 2
        for i in range(0, int(length)):
            if (i + 1) < length and (i + 1) % 2 == 1:
                next_moves.append(State(root.n, [i + 1], root.max_depth, not root.is_max_player))
    else:
        for token, avail in enumerate(root.tokens):
            if avail == 1:
                divisor = min(last_move, token + 1)
                numerator = max(last_move, token + 1)
                if numerator % divisor == 0:
                    # Deep copy of taken tokens
                    taken_tokens = deepcopy(root.taken_tokens)
                    # Player takes token
                    taken_tokens.append(token + 1)
                    # Create new state for next player with updated taken nodes
                    next_moves.append(State(root.n, taken_tokens, root.max_depth, not root.is_max_player))

    return next_moves

#   Max --> [3]
#   Min --> [3,1], [3,9]
#   1. Max was the last player and chose 3
#   2. Min can take 1 or 9
#   3. Generate all new states for Max such that the taken tokens are 1 and 9, --> 2 new nodes for max player with taken tokens [3,1] and [3,9]

#                           Max ([3])
#           Min([3,1])                      Min([3,9])
#    Max([3,1,2]) Max([3,1,4]) ...         Max([3,9,1])
#                                       Min([3,9,2]) ...