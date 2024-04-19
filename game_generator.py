from random import *
from copy import deepcopy
class SudokuGenerator:
    def __init__(self):

        pass 

    def generateSudoku(self):
        board = [[0] * 9 for i in range(9)]

        horizontal = [set(range(9)) for i in range(9)]
        vertical = [set(range(9)) for i in range(9)]
        regional = [set(range(9)) for i in range(9)]

        numFill = randrange(18, 25)

        for cnt in range(numFill):
            i, j = randrange(9), randrange(9)
            while board[i][j] != 0:
                i, j = randrange(9), randrange(9)
            k = i // 3 * 3 + j // 3

            intersect = horizontal[i] & vertical[j] & regional[k]
            if not intersect:
                break
            num = choice(list(intersect))
            board[i][j] =   num + 1
            horizontal[i].remove(num)
            vertical[j].remove(num)
            regional[k].remove(num)
        return board
    


