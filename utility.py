#!/usr/bin/env python2
"""
Utility functions to read sudoku file and print to screen.
"""

from sys import stdout


def read_sudoku_file(filepath):
    """
    Reads sudoku values from file as list of list. No consistency and sanity control.
    Sudoku input is expected to have digits (1-9) and spaces every text line.
    So it will produce 2-dimentional list with a character in each cell.

    :param filepath: path of sudoku file
    """
    ret = []
    try:
        with open(filepath, 'r') as _f:
            for rline in _f.readlines():
                lst = []
                lst.extend(rline)
                lst = lst[:-1]  # remove last newline
                ret.append(lst)
    except IOError as exception:
        print exception
    return ret


def _print_one_line_of_possibles(possibles_line, i, j, n_size):
    for cellj, pll in enumerate(possibles_line):
        if not isinstance(pll, list):
            if i == 0:
                stdout.write('={}='.format(pll) + '|')
            else:
                stdout.write('   |')
        else:
            stdout.write(('{:<' + str(n_size) + '}').format(
                ''.join(pll[i * n_size:j * n_size])) + '|')
        if (cellj + 1) % n_size == 0:
            stdout.write('|')
    print


def print_possible_sets_array(possibles_lst):
    """
    Print sudoku possible sets array by printing every possibility in the cell it belongs.

    :param possibles_lst: The possibles of 2-dimentional list. Every cell is list of possibles
    """
    n_size = 3
    print '-..-0-.-1-.-2-..-3-.-4-.-5-..-6-.-7-.-8-..'
    for i, lst in enumerate(possibles_lst):
        stdout.write(' ||')
        _print_one_line_of_possibles(lst, 0, 1, n_size)
        stdout.write(str(i) + '||')
        _print_one_line_of_possibles(lst, 1, 2, n_size)
        stdout.write(' ||')
        _print_one_line_of_possibles(lst, 2, 3, n_size)
        print '-..---.---.---..---.---.---..---.---.---..'
        if (i + 1) % n_size == 0:
            print '-..---.---.---..---.---.---..---.---.---..'
