from ass2.algorithms.AStar import a_star_search_h1, a_star_search_h2
from ass2.algorithms.DFS import *
import datetime
import random

from ass2.algorithms.IterativeDeepening import iterative_deepening


def create_test_cases(n):
    numbers = [i for i in range(1, (n * n) + 1)]
    goal = []
    for i in range(0, int(len(numbers) / n)):
        row_vals = []
        for j in range(0, n):
            row_vals.append(numbers[i * n + j])
        goal.append(tuple(row_vals))

    test_cases = []
    seen = set()
    while len(test_cases) < 20:
        random.shuffle(numbers)
        case = []
        row = []
        for i in range(0, len(numbers)):
            if i != 0 and i % n == 0:
                case.append(tuple(row))
                row = [numbers[i]]
            else:
                row.append(numbers[i])
        case.append(tuple(row))

        if tuple(case) not in seen:
            seen.add(tuple(case))
            test_cases.append(tuple(case))

    return test_cases, tuple(goal)


def parse_grid_input(input_grid):
    string_rows = input_grid.split(");")
    rows = []
    goal_arr = []
    for i in range(0, len(string_rows)):
        string_row = string_rows[i].replace("(", "").replace(")", "").replace(" ", "").split(";")
        parsed_row = [int(i) for i in string_row]
        rows.append(tuple(parsed_row))
        for num in parsed_row:
            goal_arr.append(num)

    goal_arr.sort()
    goal_rows = []
    row = []
    for i in range(0, len(goal_arr)):
        if i != 0 and i % len(rows) == 0:
            goal_rows.append(tuple(row))
            row = [goal_arr[i]]
        else:
            row.append(goal_arr[i])
    goal_rows.append(tuple(row))

    return tuple(rows), tuple(goal_rows)


def search_algorithm(algorithm, initial, goal, file_path, is_iter=False):
    time_before = datetime.datetime.now()
    result_node, search_path = algorithm(initial, goal)
    time_after = datetime.datetime.now()
    total_cost = 0
    result_path = []
    if result_node is not None:
        while result_node is not None:
            result_path.insert(0, result_node.state)
            total_cost += result_node.heuristic(result_node, result_node.p1,
                                                result_node.p2) if result_node.heuristic is not None and result_node.p1 is not None else 1
            result_node = result_node.parent
    else:
        result_path.append("No Solution")
    with open(file_path + '.txt', "w") as f:
        f.write("Time taken: %s\n" % (time_after - time_before))
        f.write("Result steps:\n")
        for i in range(0, len(result_path)):
            f.write("%d: %s\n" % (i, result_path[i]))

    search_path_length = 0 if is_iter else len(search_path)
    with open(file_path + '-search_path.txt', "w") as f:
        f.write("Search steps:\n")
        for i in range(0, len(search_path)):
            if is_iter:
                f.write("Attempt: %d\n" % i)
                search_path_length += len(search_path[i])
                for j in range(0, len(search_path[i])):
                    f.write("%d: %s\n" % (j, search_path[i][j]))
            else:
                f.write("%d: %s\n" % (i, search_path[i]))

    return (time_after - time_before).total_seconds(), total_cost, len(result_path), search_path_length


def one_test_case():
    test_cases = create_test_cases()
    parsed_goal = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    parsed_input = test_cases[0]
    search_algorithm(depth_first_search, parsed_input, parsed_goal, 'result/dfs/depth_first_search')
    search_algorithm(iterative_deepening, parsed_input, parsed_goal, 'result/iter/iterative_deepening_search', True)
    search_algorithm(a_star_search_h1, parsed_input, parsed_goal, 'result/a_star/h1/a_star_search_h1')
    search_algorithm(a_star_search_h2, parsed_input, parsed_goal, 'result/a_star/h2/a_star_search_h2')


def multi_test_case(n=3):
    test_cases, goal = create_test_cases(n)
    i = 1
    for test in test_cases:
        search_algorithm(depth_first_search, test, goal, 'result/dfs/depth_first_search-' + str(i))
        search_algorithm(iterative_deepening, test, goal, 'result/iter/iterative_deepening_search-' + str(i), True)
        search_algorithm(a_star_search_h1, test, goal, 'result/a_star/h1/a_star_search_h1-' + str(i))
        search_algorithm(a_star_search_h2, test, goal, 'result/a_star/h2/a_star_search_h2-' + str(i))
        i += 1


def file_path_test_case(file_path):
    calculate_result(file_path, depth_first_search, "depth_first_search", "dfs/")
    calculate_result(file_path, iterative_deepening, "iterative_deepening_search", "iter/", True)
    calculate_result(file_path, a_star_search_h1, "a_star_search_h1", "a_star/h1/")
    calculate_result(file_path, a_star_search_h2, "a_star_search_h2", "a_star/h2/")


def calculate_result(file_path, algo, algo_name, folder, is_iter=False):
    total_time = 0
    total_cost = 0
    total_search_path_length = 0
    total_result_path_length = 0
    total_no_solution = 0
    total_solution = 0
    with open(file_path, "r", encoding="utf8") as f:
        for i, case in enumerate(f):
            parsed_input, parsed_goal = parse_grid_input(case)
            time, cost, result_length, search_length = search_algorithm(algo, parsed_input, parsed_goal,
                                                                        'result/' + folder + algo_name + '-' + str(i),
                                                                        is_iter)
            if result_length > 1:
                total_time += time
                total_cost += cost
                total_result_path_length += result_length
                total_search_path_length += search_length
                total_solution += 1
            else:
                total_no_solution += 1

    with open("result/search.txt", "a") as f:
        f.write("\nAlgorithm: " + algo_name + "\n")
        f.write("Total time: " + str(total_time) + " Time average: " + str((total_time / total_solution)) + "\n")
        f.write("Total cost: " + str(total_cost) + " Cost average: " + str((total_cost / total_solution)) + "\n")
        f.write("Total result path length: " + str(total_result_path_length) + " Result path length average: " +
                str((total_result_path_length / total_solution)) + "\n")
        f.write("Search result path length: " + str(total_search_path_length) + " Search path length average: " +
                str((total_search_path_length / total_solution)) + "\n")
        f.write("Total solution: " + str(total_solution) + "\n")
        f.write("Total no solution: " + str(total_no_solution) + "\n")


def input_test_case():
    initial_input = input("Enter S-Puzzle to solve: ")
    parsed_input, parsed_goal = parse_grid_input(initial_input)
    search_algorithm(depth_first_search, parsed_input, parsed_goal, 'result/dfs/depth_first_search')
    search_algorithm(iterative_deepening, parsed_input, parsed_goal, 'result/iter/iterative_deepening_search', True)
    search_algorithm(a_star_search_h1, parsed_input, parsed_goal, 'result/a_star/h1/a_star_search_h1')
    search_algorithm(a_star_search_h2, parsed_input, parsed_goal, 'result/a_star/h2/a_star_search_h2')


def test():
    # initial_input = "((24; 15; 23; 14; 9); (3; 8; 20; 11; 12); (19; 6; 21; 17; 18); (13; 25; 7; 5; 22); (16; 2; 10; 4; 1))"
    initial_input = "((4; 6; 7); (9; 8; 2); (3; 5; 1))"
    parsed_input, parsed_goal = parse_grid_input(initial_input)
    search_algorithm(depth_first_search, parsed_input, parsed_goal, 'result/dfs/depth_first_search')
    search_algorithm(iterative_deepening, parsed_input, parsed_goal, 'result/iter/iterative_deepening_search', True)
    search_algorithm(a_star_search_h1, parsed_input, parsed_goal, 'result/a_star/h1/a_star_search_h1')
    search_algorithm(a_star_search_h2, parsed_input, parsed_goal, 'result/a_star/h2/a_star_search_h2')


option = int(input(
    "Choose one of the following options:\n\t[0] Manually enter a puzzle\n\t[1] Run against a single test case"
    "\n\t[2] Run against 20 test cases\n\t[3] Run with file \nEnter input: "))

if option == 0:
    input_test_case()
elif option == 1:
    one_test_case()
elif option == 2:
    multi_test_case()
else:
    file_path_test_case('data/test_input')
