#!/usr/bin/env python

from copy import deepcopy
from random import randint
import sys

TOUCHES = { 0: [1, 4, 5], 1: [0, 2, 4, 5, 6], 2: [1, 3, 5, 6, 7],
            3: [2, 6, 7], 4: [0, 1, 5, 8, 9], 5: [0, 1, 2, 4, 6, 8, 9, 10], 
            6: [1, 2, 3, 5, 7, 9, 10, 11], 7: [2, 3, 6, 10, 11],
            8: [4, 5, 9, 12, 13], 9: [4, 5, 6, 8, 10, 12, 13, 14],
            10: [5, 6, 7, 8, 11, 13, 14, 15], 11: [6, 7, 10, 14, 15],
            12: [8, 9, 13], 13: [8, 9, 10, 12, 14], 14: [9, 10, 11, 13, 15],
            15: [10, 11, 14] 
           }

ANSWER_WORDS = []

def load_words():
    words = []
    with open('dictionary.txt') as dictionary:
        for line in dictionary:
            line = line.strip()
            if len(line) > 16 or len(line) <= 2:
                continue
            else:
                words.append(line.strip())

    return words

def roll():
    return randint(0,5)

def roll_cubes():

    cubes = ['aaeegn', 'elrtty', 'aoottw', 'abbjoo',
             'ehrtvw', 'cimotu', 'distty', 'eiosst',
             'delrvy', 'achops', 'himnqu', 'eeinsu',
             'eeghnw', 'affkps', 'hlnnrz', 'deilrx']

    board = []
    for cube in cubes:
        board.append(cube[roll()])
    
    return board

def print_board(board):
    for index, letter in enumerate(board):
        print letter,
        if ((index + 1) % 4) == 0:
            print
        
def all_letters_on_board(word, board):
    game_board = deepcopy(board)
    for letter in word:
        if letter not in game_board:
            return False
        else:
            game_board.remove(letter)

    return True

# ensure all letters in word can be found on board
def create_word_list(word, board):
    letter_lists =[]
    for letter in word: 
        positions = []
        for idx, val in enumerate(board):
            if letter == val:
                positions.append(idx)
        letter_lists.append(positions)

    return letter_lists

# ensure a path can be drawn from the previous char to the next char of a word
def sketch_paths(letter_lists):
    cur_idx = 0
    nxt_idx = 1
    while nxt_idx < len(letter_lists):
        cur = deepcopy(letter_lists[cur_idx])
        nxt = deepcopy(letter_lists[nxt_idx])
        for cur_pos in cur:
            path = False
            for nxt_pos in nxt:
                if nxt_pos in TOUCHES[cur_pos]:
                    path = True
                    # current pos has at least one match, break and check next cur pos
                    break

            # after we check all nxts
            if not path:
                letter_lists[cur_idx].remove(cur_pos)
                if not letter_lists[cur_idx]:
                    return None

        cur_idx += 1
        nxt_idx += 1

    return letter_lists

def remove_path_repeats(letter_lists):
    singles = []
    # generate list of single position dependencies
    for lst in letter_lists:
        if len(lst) == 1:
            singles.append(lst[0])

    # remove single dependencies from lists 
    for idx, lst in enumerate(letter_lists):
        if len(lst) > 1:
            for val in lst:
                if val in singles:
                    letter_lists[idx].remove(val)

    # remove single duplicates
    single_dupes = []
    for lst in letter_lists:
        # catch case where all were removed
        if len(lst) == 0:
            return None
        if len(lst) == 1:
            single_dupes.append(lst[0])

    check_dupes = len(single_dupes)
    dupes_removed = list(set(single_dupes))
    if check_dupes != len(dupes_removed):
        return None
    
    return letter_lists

def find_words(words, board):
    for word in words:
        # basic check that letters in word exist on board
        if not all_letters_on_board(word, board):
            continue

        # create coordinate list
        letter_lists = create_word_list(word, board)

        # sketch paths once
        letter_lists = sketch_paths(letter_lists)
        if not letter_lists:
            continue

        # clear repeats / duplicates
        letter_lists = remove_path_repeats(letter_lists)
        if not letter_lists:
            continue

        # finalize paths
        letter_lists = sketch_paths(letter_lists)
        if not letter_lists:
            continue

        ANSWER_WORDS.append(word)

    print ANSWER_WORDS

if __name__ == "__main__":
    board = roll_cubes()
    find_words(load_words(), board)
    print_board(board)
