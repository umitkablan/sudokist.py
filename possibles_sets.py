#!/usr/bin/env python2

complete_set = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])


def get_set_at_line_i(lst, i):
    ret = set(lst[i])
    ret.remove(' ')
    return ret


def get_set_at_column_j(lst, j):
    ret = set()
    for l in lst:
        ret.add(l[j])
    ret.remove(' ')
    return ret


def get_set_at_NxN_grid_ij(lst, i, j, N):
    ret = set()
    for l in lst[i * N: i * N + N]:
        for k in range(N):
            for c in l[j * N + k]:
                ret.add(c)
    ret.remove(' ')
    return ret


def get_possible_numbers_set_at(sudoku_lst, i, j):
    s = get_set_at_line_i(sudoku_lst, i)
    s = s.union(get_set_at_column_j(sudoku_lst, j))
    s = s.union(get_set_at_NxN_grid_ij(sudoku_lst, i / 3, j / 3, 3))
    return complete_set.difference(s)


def get_possible_sets_by_counting(sudoku_lst):
    possibles = []
    for i, ll in enumerate(sudoku_lst):
        poss = []
        for j, c in enumerate(ll):
            lst = []
            if c == ' ':
                lst.extend(get_possible_numbers_set_at(sudoku_lst, i, j))
                lst.sort()
            poss.append(lst)
        possibles.append(poss)
    return possibles
