#!/usr/bin/env python2

import sys

from possibles_sets import (get_possible_sets_by_counting, complete_set)
from logic import get_solutions_by_only_probables, get_solutions_by_one_elem_possibles


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
    soln = 1
    possibles = get_possible_sets_by_counting(read_arr)
    soll = get_solutions_by_one_elem_possibles(possibles)
    if not soll:
        soll = get_solutions_by_only_probables(possibles)
        if not soll:
            break
        soln = 2
    for (i, j), v in soll:
        if soln == 1:
            print "[Counting]",
        else:
            print "[By Probable]",
        print "({},{}): {}".format(i, j, v)
        read_arr[i][j] = v
print_possible_sets_array(read_arr, possibles)
