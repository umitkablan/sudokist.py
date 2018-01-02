#!/usr/bin/env python2

import sys

complete_set = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])


def read_sudoku_file(filepath):
    ret = []
    try:
        with open(filepath, 'r') as f:
            for l in f.readlines():
                sl = []
                sl.extend(l)
                sl = sl[:-1]  # remove last newline
                ret.append(sl)
    except Exception as e:
        print e
    return ret


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


def get_possible_numbers_set_at(sudoku_lst, ij):
    i, j = ij
    s = get_set_at_line_i(sudoku_lst, i)
    s = s.union(get_set_at_column_j(sudoku_lst, j))
    s = s.union(get_set_at_NxN_grid_ij(sudoku_lst, i / 3, j / 3, 3))
    return complete_set.difference(s)


def get_intersection_of_diffsets(s0, set_lst):
    res = complete_set
    for s in set_lst:
        if not s:
            continue
        res = res.intersection(s0.difference(s))
        if not res:
            return res
    return res


def get_only_probable_in_line(pll):
    ret = []
    for i, pl in enumerate(pll):
        if len(pl) < 1:
            continue
        res = get_intersection_of_diffsets(
            set(pl), [set(l) for l in pll[:i] + pll[i + 1:] if len(l) > 0])
        if len(res) == 1:
            ret.append([i, res.pop()])
    return ret


def get_only_probable_in_column_j(possibles, j):
    col = []
    for pll in possibles:
        col.append(pll[j])
    return get_only_probable_in_line(col)


def get_only_probable_in_NxN_grid_ij(possibles, i, j, N):
    col = []
    for l in possibles[i * N: i * N + N]:
        for k in l[j * N:j * N + N]:
            col.append(k)
    return get_only_probable_in_line(col)


def get_only_probable_at(possibles_llst, ij):
    i, j = ij
    ret = [[(i, j_), s]
           for j_, s in get_only_probable_in_line(possibles_llst[i])]
    ret.extend([[(i_, j), s]
                for i_, s in get_only_probable_in_column_j(possibles_llst, j)])
    ith, jth = i / 3, j / 3
    ret.extend([[((i_ / 3) + (ith * 3), (i_ % 3) + (jth * 3)), s]
                for i_, s in get_only_probable_in_NxN_grid_ij(possibles_llst, ith, jth, 3)])
    return ret


def get_possible_sets_by_counting(sudoku_lst):
    possibles = []
    for i, ll in enumerate(sudoku_lst):
        poss = []
        for j, c in enumerate(ll):
            lst = []
            if c == ' ':
                lst.extend(get_possible_numbers_set_at(sudoku_lst, (i, j)))
                lst.sort()
            poss.append(lst)
        possibles.append(poss)
    return possibles


def get_solutions_by_one_elem_possibles(possibles_lst):
    ret = []
    for i, ll in enumerate(possibles_lst):
        for j, lc in enumerate(ll):
            if len(lc) == 1:
                ret.append(((i, j), lc[0]))
    return ret


def get_solutions_by_only_probables(possibles_lst):
    ret = []
    for i, ll in enumerate(possibles_lst):
        for j, l in enumerate(ll):
            if len(l) > 1:
                ret.extend(get_only_probable_at(possibles_lst, (i, j)))
    dd = dict()
    for ij, v in ret:
        dd[ij] = v
    return [(ij, v) for ij, v in dd.iteritems()]


def print_possible_sets_array(sudoku_lst, possibles_lst):
    def print_one_line_of_possibles(possibles_line, sudoku_line, begi, endi):
        for i, pll in enumerate(possibles_line):
            txt = '   '
            if pll:
                txt = '{:<3}'.format(''.join(pll[begi:endi]))
            elif begi == 0:
                txt = '={}='.format(sudoku_line[i])
            txt += '|'
            sys.stdout.write(txt)
        print

    for i, ll in enumerate(possibles_lst):
        print_one_line_of_possibles(ll, sudoku_lst[i], 0, 3)
        print_one_line_of_possibles(ll, sudoku_lst[i], 3, 6)
        print_one_line_of_possibles(ll, sudoku_lst[i], 6, 9)
        print '---.---.---.---.---.---.---.---.---.'


read_arr = read_sudoku_file('data/hard_01.txt')
if not read_arr:
    exit(1)

while True:
    possibles = get_possible_sets_by_counting(read_arr)
    soll = get_solutions_by_one_elem_possibles(possibles)
    if not soll:
        soll = get_solutions_by_only_probables(possibles)
        if not soll:
            break
    for (i, j), v in soll:
        print "({},{}): {}".format(i, j, v)
        read_arr[i][j] = v
print_possible_sets_array(read_arr, possibles)
