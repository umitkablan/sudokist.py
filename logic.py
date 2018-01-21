#!/usr/bin/env python2
"""
Implements Sudoku solving logic from possibles' list. Codes 3 basic techniques as well as 1
composition.
"""

from copy import deepcopy

from possibles_sets import COMPLETE_SET, get_possible_sets_by_counting
# from utility import print_possible_sets_array


def _get_column_as_line(possibles, j):
    col = []
    for pll in possibles:
        col.append(pll[j])
    return col


def _get_n_to_n_grid_as_line(possibles, i, j, n_size):
    col = []
    for setline in possibles[i * n_size: i * n_size + n_size]:
        for k in setline[j * n_size:j * n_size + n_size]:
            col.append(k)
    return col


def _get_intersection_of_diffsets(set0, set_lst):
    res = COMPLETE_SET
    for set_ in set_lst:
        if not set_:
            continue
        res = res.intersection(set0.difference(set_))
        if not res:
            return res
    return res


def _get_only_probable_in_line_at_i(pll, i):
    ret = None
    res = _get_intersection_of_diffsets(
        set(pll[i]), [set(l) for l in pll[:i] + pll[i + 1:] if len(l) > 0])
    if len(res) == 1:
        ret = res.pop()
    return ret


def _get_only_probable_at(possibles_llst, ij_pos):
    i, j = ij_pos
    ret = _get_only_probable_in_line_at_i(possibles_llst[i], j)
    if ret is not None:
        return [(ij_pos, ret)]
    ret = _get_only_probable_in_line_at_i(_get_column_as_line(possibles_llst, j),
                                          i)
    if ret is not None:
        return [(ij_pos, ret)]
    ith, jth = i / 3, j / 3
    ret = _get_only_probable_in_line_at_i(_get_n_to_n_grid_as_line(possibles_llst, ith, jth, 3),
                                          (i - (ith * 3)) * 3 + (j - (jth * 3)))
    if ret is not None:
        return [(ij_pos, ret)]
    return []


def _get_columns_same_set_in_size_n(set_lst, n_size):
    selecteds = []
    for i in range(0, len(set_lst) - n_size + 1):
        if len(set_lst[i]) != n_size:
            continue
        selecteds.append(set_lst[i])
        for j in range(i + 1, len(set_lst)):
            if selecteds[0] == set_lst[j]:
                selecteds.append(set_lst[j])
                if len(selecteds) == n_size:
                    return selecteds[0]
        selecteds = []
    return None


def _get_unique_probable_in_line_at_i(pll, i):
    ret = None
    set_i = set(pll[i])
    rest = [set(l) for l in pll[:i] + pll[i + 1:] if len(l) > 0]
    for n_size in range(2, len(set_i) + 1):
        set0 = _get_columns_same_set_in_size_n(rest, n_size)
        if set0:
            set_diff = set_i.difference(set0)
            if len(set_diff) == 1:
                ret = set_diff.pop()
                break
    return ret


def _get_unique_probable_at(possibles_lst, ij_pos):
    i, j = ij_pos
    ret = _get_unique_probable_in_line_at_i(possibles_lst[i], j)
    if ret is not None:
        return [(ij_pos, ret)]
    ret = _get_unique_probable_in_line_at_i(
        _get_column_as_line(possibles_lst, j), i)
    if ret is not None:
        return [(ij_pos, ret)]
    ith, jth = i / 3, j / 3
    ret = _get_unique_probable_in_line_at_i(
        _get_n_to_n_grid_as_line(possibles_lst, ith, jth, 3), (i - (ith * 3)) * 3 + (j - (jth * 3)))
    if ret is not None:
        return [(ij_pos, ret)]
    return []


def _get_solutions_by_unique_probables(possibles_lst):
    ret = []
    for i, line in enumerate(possibles_lst):
        for j, set_ in enumerate(line):
            if len(set_) > 1:
                ret.extend(_get_unique_probable_at(possibles_lst, (i, j)))
    return ret


def _get_solutions_by_only_probables(possibles_lst):
    ret = []
    for i, line in enumerate(possibles_lst):
        for j, set_ in enumerate(line):
            if len(set_) > 1:
                ret.extend(_get_only_probable_at(possibles_lst, (i, j)))
    return ret


def _get_solutions_by_one_elem_possibles(possibles_lst):
    ret = []
    for i, line in enumerate(possibles_lst):
        for j, set_ in enumerate(line):
            if len(set_) == 1 and isinstance(set_, list):
                ret.append(((i, j), set_[0]))
    return ret


def _find_least_set_in_possibles(possibles_lst):
    ij_pos, min_, retset = (-1, -1), 10, None
    for i, line in enumerate(possibles_lst):
        for j, set_ in enumerate(line):
            setlen = len(set_)
            if setlen < min_ and setlen > 1:
                min_ = setlen
                ij_pos = (i, j)
                retset = set_
    return ij_pos, retset


def _check_solution_violation(possibles_lst):
    for line in possibles_lst:
        for set_ in line:
            if isinstance(set_, list) and not set_:
                return True
    return False


def check_solution_done(possibles_lst):
    """
    Checks whether Sudoku possibles list is done - no further solutions.
    """
    for line in possibles_lst:
        for set_ in line:
            if len(set_) != 1:
                return False
    return True


def _rearrange_possibilities(possibles_lst):
    for line in possibles_lst:
        for j, set_ in enumerate(line):
            if isinstance(set_, list):
                line[j] = ' '
    return get_possible_sets_by_counting(possibles_lst)


def _try_solve_guess(possibles_lst):
    ret = []
    while True:
        solutions, desc = get_simple_solutions(possibles_lst)
        if not solutions:
            break
        apply_solution_to_possibles(possibles_lst, solutions)
        possibles_lst = _rearrange_possibilities(possibles_lst)
        if _check_solution_violation(possibles_lst):
            ret = []
            break
        # if check_solution_done(possibles_lst):
        #     break
        # print_possible_sets_array(possibles_lst)
        ret.extend(solutions)
    return ret


def _get_solutions_by_guessing(possibles_lst):
    ret = []
    (i, j), least_set = _find_least_set_in_possibles(possibles_lst)
    if least_set is None:
        return ret
    copy_lst = deepcopy(possibles_lst)
    for guess in least_set:
        copy_lst[i][j] = guess
        copy_lst = _rearrange_possibilities(copy_lst)
        ret = _try_solve_guess(copy_lst)
        if ret:
            ret.insert(0, ((i, j), guess))
            break
        copy_lst, ret = deepcopy(possibles_lst), []
    return ret


SOLUTIONS_DESCRIPTIONS = [
    {'Counting': 'Select cells where only one fits'},
    {'Diff Probable': 'Select cells where has a probability which none others has'},
    {'Unique Remains': 'Select cells where only option for others make it to have one possibility'},
    {'Guessing': 'Select cells by guessing'}
]


def get_simple_solutions(possibles_lst):
    """
    Returns solution step(s) and it's associated method name using basic techniques.

    :param possibles_lst: Possibles list of Sudoku state
    """
    i = 0
    solutions = _get_solutions_by_one_elem_possibles(possibles_lst)
    if not solutions:
        i = 1
        solutions = _get_solutions_by_only_probables(possibles_lst)
        if not solutions:
            i = 2
            solutions = _get_solutions_by_unique_probables(possibles_lst)
    return solutions, SOLUTIONS_DESCRIPTIONS[i].keys()[0]


def get_solutions(possibles_lst):
    """
    Returns solutions applying all techniques.

    :param possibles_lst: Possibles list of Sudoku state
    """
    solutions, desc_key = get_simple_solutions(possibles_lst)
    if not solutions:
        solutions, desc_key = (_get_solutions_by_guessing(possibles_lst),
                               SOLUTIONS_DESCRIPTIONS[3].keys()[0])
    return solutions, desc_key


def apply_solution_to_possibles(possibles_lst, solutions):
    """
    Apply solutions to possibles list.
    """
    for (i, j), solution_chr in solutions:
        possibles_lst[i][j] = solution_chr
