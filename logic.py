#!/usr/bin/env python2

from possibles_sets import complete_set


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
