#!/usr/bin/env python2
"""
Print step by step solutions of a Sudoku game. Initial status is read from a file and progressively
solved.
"""

from utility import read_sudoku_file, print_possible_sets_array
from possibles_sets import get_possible_sets_by_counting
from logic import get_solutions, apply_solution_to_possibles


def solve_sudoku(fpath):
    """
    Reads sudoku characters from file and returns solved state printing the steps.

    :param fpath: path of sudoku data which is plain text
    """
    read_arr = read_sudoku_file(fpath)
    if not read_arr:
        return []

    while True:
        possibles = get_possible_sets_by_counting(read_arr)
        solutions, desc_key = get_solutions(possibles)
        if not solutions:
            break
        print "[{:<14}]".format(desc_key),
        for (i, j), solution_chr in solutions:
            print "({},{}):{};".format(i, j, solution_chr),
        print
        apply_solution_to_possibles(read_arr, solutions)
    return possibles


if __name__ == '__main__':
    POSSIBLES = solve_sudoku('data/veryhard_01.txt')
    if not POSSIBLES:
        exit(1)
    print_possible_sets_array(POSSIBLES)
