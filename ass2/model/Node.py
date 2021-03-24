class Node:

    def __init__(self, initial_state, depth, heuristic=None, p1=None, p2=None, parent=None):
        self.state = initial_state
        self.cost = 0
        self.depth = depth
        self.heuristic = heuristic
        self.p1 = p1
        self.p2 = p2
        self.parent = parent

    def is_goal_state(self, goal):
        return hash(goal) == hash(self.state)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.state == other.state
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return self.state.__str__()

    def __lt__(self, other):
        return self.heuristic(self, self.p1, self.p2) < self.heuristic(other, other.p1, other.p2)
