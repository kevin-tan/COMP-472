from ass3.algorithm.AlphaBetaPruning import alpha_beta_pruning


def parse_input_string(input_string):
    nums = input_string.split(" ")[1:]
    n = int(nums[0])
    num_taken_tokens = int(nums[1])
    taken_tokens = [int(i) for i in nums[2:2 + num_taken_tokens]]
    max_depth = int(nums[-1])
    is_max_player = num_taken_tokens % 2 == 0
    print("n:", n, ", taken:", taken_tokens, "max depth:", max_depth, ", is max player:", is_max_player)
    return n, taken_tokens, max_depth, is_max_player


def run_with_file(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        for i, case in enumerate(f):
            n, taken_tokens, max_depth, is_max_player = parse_input_string(case)
            score, move, visited, evaled, max_level, branching_factor = alpha_beta_pruning(n, taken_tokens, max_depth,
                                                                                           is_max_player)
            with open('result/testcase-' + str(i) + '.txt', "w") as result_file:
                # result_file.write("Move: %d\n" % move.taken_tokens[-1])
                # result_file.write("Value: %.1f\n" % score)
                # result_file.write("Number of Nodes Visited:: %d\n" % visited)
                # result_file.write("Number of Nodes Evaluated: %d\n" % evaled)
                # result_file.write("Max Depth Reached: %d\n" % max_level)
                # result_file.write("Avg Effective Branching Factor: %.1f\n" % branching_factor)
                print("Move: %d" % move.taken_tokens[-1])
                print("Value: %.1f" % score)
                print("Number of Nodes Visited:: %d" % visited)
                print("Number of Nodes Evaluated: %d" % evaled)
                print("Max Depth Reached: %d" % max_level)
                print("Avg Effective Branching Factor: %.1f\n" % branching_factor)


run_with_file("testcases/testcase.txt")
