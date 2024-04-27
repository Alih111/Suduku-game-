from random import randrange
from random import shuffle
from SudukuLogic import SudokuSolver
class SudokuGenerator:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]


    def generateSudoku(self):
        horizontal = [set(range(1, 10)) for _ in range(9)]
        vertical = [set(range(1, 10)) for _ in range(9)]
        regional = [set(range(1, 10)) for _ in range(9)]
        
        if self.solveSudoku( horizontal, vertical, regional):
            solved_board = [row[:] for row in self.board]
            self.remove_elements()
            return solved_board, self.board
        else:
            return None, None

    def not_full(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return True
        return False
    
    
    def solveSudoku(self, horizontal, vertical, regional):
        if not self.not_full():
            return True

        row, col = self.find_empty_location()
        box = row // 3 * 3 + col // 3

        intersect = horizontal[row] & vertical[col] & regional[box]
        intersect = list(intersect)
        shuffle(intersect)
        for num in intersect:
            self.board[row][col] = num
            horizontal[row].remove(num)
            vertical[col].remove(num)
            regional[box].remove(num)
            if self.solveSudoku(horizontal, vertical, regional):
                return True
            self.board[row][col] = 0
            horizontal[row].add(num)
            vertical[col].add(num)
            regional[box].add(num)
        return False

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1

    def remove_elements(self):
        empty_cells = 40
        solver = SudokuSolver(self.board)
        while empty_cells > 0:
            i, j = randrange(9), randrange(9)
            while self.board[i][j] == 0:
                i, j = randrange(9), randrange(9)
            temp = self.board[i][j]
            self.board[i][j] = 0
            
            temp_board = [row[:] for row in self.board]
            
            if solver.count_possible_solutions(temp_board) == 1:
                
                empty_cells -= 1
            else:
                self.board[i][j] = temp
                
