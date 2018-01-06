#!/usr/bin/env python2

from possibles_sets import complete_set


def get_column_as_line(possibles, j):
    col = []
    for pll in possibles:
        col.append(pll[j])
    return col


def get_NxN_grid_as_line(possibles, i, j, N):
    col = []
    for l in possibles[i * N: i * N + N]:
        for k in l[j * N:j * N + N]:
            col.append(k)
    return col


def get_intersection_of_diffsets(s0, set_lst):
    res = complete_set
    for s in set_lst:
        if not s:
            continue
        res = res.intersection(s0.difference(s))
        if not res:
            return res
    return res


def get_only_probable_in_line_at_i(pll, i):
    ret = None
    res = get_intersection_of_diffsets(
        set(pll[i]), [set(l) for l in pll[:i] + pll[i + 1:] if len(l) > 0])
    if len(res) == 1:
        ret = res.pop()
    return ret


def get_only_probable_at(possibles_llst, ij):
    i, j = ij
    ret = get_only_probable_in_line_at_i(possibles_llst[i], j)
    if ret is not None:
        return [(ij, ret)]
    ret = get_only_probable_in_line_at_i(
        get_column_as_line(possibles_llst, j), i)
    if ret is not None:
        return [(ij, ret)]
    ith, jth = i / 3, j / 3
    ret = get_only_probable_in_line_at_i(
        get_NxN_grid_as_line(possibles_llst, ith, jth, 3), (i - (ith * 3)) * 3 + (j - (jth * 3)))
    if ret is not None:
        return [(ij, ret)]
    return []


def get_columns_same_set_in_size_n(set_lst, N):
    selecteds = []
    for i in range(0, len(set_lst) - N + 1):
        if len(set_lst[i]) != N:
            continue
        selecteds.append(set_lst[i])
        for j in range(i + 1, len(set_lst)):
            if selecteds[0] == set_lst[j]:
                selecteds.append(set_lst[j])
                if len(selecteds) == N:
                    return selecteds[0]
        selecteds = []
    return None


def get_unique_probable_in_line_at_i(pll, i):
    ret = None
    s = set(pll[i])
    rest = [set(l) for l in pll[:i] + pll[i + 1:] if len(l) > 0]
    for n in range(2, len(s) + 1):
        s0 = get_columns_same_set_in_size_n(rest, n)
        if s0:
            r = s.difference(s0)
            if len(r) == 1:
                ret = r.pop()
                break
    return ret


def get_unique_probable_at(possibles_lst, ij):
    i, j = ij
    ret = get_unique_probable_in_line_at_i(possibles_lst[i], j)
    if ret is not None:
        return [(ij, ret)]
    ret = get_unique_probable_in_line_at_i(
        get_column_as_line(possibles_lst, j), i)
    if ret is not None:
        return [(ij, ret)]
    ith, jth = i / 3, j / 3
    ret = get_unique_probable_in_line_at_i(
        get_NxN_grid_as_line(possibles_lst, ith, jth, 3), (i - (ith * 3)) * 3 + (j - (jth * 3)))
    if ret is not None:
        return [(ij, ret)]
    return []


def get_solutions_by_unique_probables(possibles_lst):
    ret = []
    for i, ll in enumerate(possibles_lst):
        for j, l in enumerate(ll):
            if len(l) > 1:
                ret.extend(get_unique_probable_at(possibles_lst, (i, j)))
    return ret


def get_solutions_by_only_probables(possibles_lst):
    ret = []
    for i, ll in enumerate(possibles_lst):
        for j, l in enumerate(ll):
            if len(l) > 1:
                ret.extend(get_only_probable_at(possibles_lst, (i, j)))
    return ret


def get_solutions_by_one_elem_possibles(possibles_lst):
    ret = []
    for i, ll in enumerate(possibles_lst):
        for j, lc in enumerate(ll):
            if len(lc) == 1:
                ret.append(((i, j), lc[0]))
    return ret


solutions_descriptions = [
    {'Counting': 'Select cells where only one fits'},
    {'Diff Probable': 'Select cells where has a probability which none others has'},
    {'Unique Remains': 'Select cells where only options for others make it to have one possibility'}
]


def get_solutions(possibles_lst):
    i = 0
    solutions = get_solutions_by_one_elem_possibles(possibles_lst)
    if not solutions:
        i = 1
        solutions = get_solutions_by_only_probables(possibles_lst)
        if not solutions:
            i = 2
            solutions = get_solutions_by_unique_probables(possibles_lst)
    return solutions, solutions_descriptions[i].keys()[0]
