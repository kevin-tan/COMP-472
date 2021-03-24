from ass2.model.Node import *


def next_node(current_node, i, j, x, y, level, heuristic=None):
    state = current_node.state
    grid = []
    for row in range(0, len(state)):
        grid_row = []
        grid.append(grid_row)
        for col in range(0, len(state[row])):
            grid_row.append(state[row][col])

    temp = grid[i][j]
    grid[i][j] = grid[x][y]
    grid[x][y] = temp
    return Node(tuple([tuple(i) for i in grid]), level, parent=current_node, heuristic=heuristic, p1=(i, j), p2=(x, y))


def generate_next_state(current_node, visited):
    state = current_node.state
    row_len = len(state)
    col_len = len(state[0])
    for row in range(0, row_len):
        for col in range(0, col_len):
            if col + 1 < col_len:
                node = next_node(current_node, row, col, row, col + 1, current_node.depth + 1)
                if node not in visited:
                    return node
            if row + 1 < row_len:
                node = next_node(current_node, row, col, row + 1, col, current_node.depth + 1)
                if node not in visited:
                    return node
    return None
