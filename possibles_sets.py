#!/usr/bin/env python2
"""
Counts and creates possible numbers' set of a given Sudoku characters list of list.
Also exports COMPLETE_SET which is all digits to be completed in Sudoku.
"""

COMPLETE_SET = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])


def _get_set_at_line_i(lst, i):
    ret = set(lst[i])
    ret.remove(' ')
    return ret


def _get_set_at_column_j(lst, j):
    ret = set()
    for item in lst:
        ret.add(item[j])
    ret.remove(' ')
    return ret


def _get_set_at_n_to_n_grid_ij(lst, i, j, n_size):
    ret = set()
    for setline in lst[i * n_size: i * n_size + n_size]:
        for k in range(n_size):
            for sudoku_chr in setline[j * n_size + k]:
                ret.add(sudoku_chr)
    ret.remove(' ')
    return ret


def get_possible_numbers_set_at(sudoku_lst, i, j):
    """
    Return missing values (from COMPLETE_SET) for cell ij at a sudoku list

    :param sudoku_lst: List of list of chars for sudoku cells
    :param i: i index
    :param j: j index
    """
    set0 = _get_set_at_line_i(sudoku_lst, i)
    set0 = set0.union(_get_set_at_column_j(sudoku_lst, j))
    set0 = set0.union(_get_set_at_n_to_n_grid_ij(sudoku_lst, i / 3, j / 3, 3))
    return COMPLETE_SET.difference(set0)


def get_possible_sets_by_counting(read_lst):
    """
    Calculate and return possible sets' 2 dimensional list of the given sudoku chars' list.

    :param read_lst: List of list of chars ([1-9 ]) of Sudoku
    """
    possibles = []
    for i, charline in enumerate(read_lst):
        poss = []
        for j, sudoku_chr in enumerate(charline):
            if sudoku_chr == ' ':
                lst = []
                lst.extend(get_possible_numbers_set_at(read_lst, i, j))
                lst.sort()
                poss.append(lst)
            else:
                poss.append(sudoku_chr)
        possibles.append(poss)
    return possibles
