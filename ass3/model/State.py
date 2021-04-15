class State:
    def __init__(self, n, taken_tokens, max_depth, is_max_player):
        self.n = n
        self.taken_tokens = taken_tokens
        self.tokens = self.create_tokens(n, taken_tokens)
        self.max_depth = max_depth
        self.is_max_player = is_max_player
        self.moves = []

    def create_tokens(self, n, taken_tokens):
        tokens = [1 for _ in range(0, n)]
        for i in taken_tokens:
            tokens[i - 1] = 0
        return tokens

    def count_successors(self, last_number):
        successors = 0
        for i, num in enumerate(self.tokens):
            current_num = i + 1
            divisor = min(last_number, current_num)
            numerator = max(last_number, current_num)
            if numerator % divisor == 0 and num == 1:
                successors += 1
        return successors

    # We count the number of primes that are possible for the given number
    # Working backwards on the array will provide us the biggest possible prime number in the composite
    def largest_prime(self, last_number):
        if last_number < 2:
            return last_number

        primes = [True] * (last_number + 1)
        for i in range(2, len(primes)):
            if primes[i]:
                j = i
                while j * i < len(primes):
                    primes[i * j] = False
                    j += 1

        for i, is_prime in enumerate(reversed(primes)):
            val = len(primes) - i - 1
            if is_prime and val <= last_number and last_number % val == 0:
                return len(primes) - i - 1
        return 1.0

    def heuristic_value(self):
        value = 0.0
        if len(self.moves) == 0:
            return -1.0 if self.is_max_player else 1.0
        if self.tokens[0] == 1:
            return value
        if len(self.taken_tokens) > 0:
            last_num = self.largest_prime(self.taken_tokens[-1])
            successors = self.count_successors(last_num)
            mult = 1.0 if successors % 2 == 1 else -1.0
            if last_num == 1:
                value = 0.5 * mult
            elif last_num == self.taken_tokens[-1]:
                value = 0.7 * mult
            else:
                value = 0.6 * mult
        return value if self.is_max_player else -value
