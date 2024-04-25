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

        i, j = self.find_empty_location()
        k = i // 3 * 3 + j // 3

        intersect = horizontal[i] & vertical[j] & regional[k]
        intersect = list(intersect)
        shuffle(intersect)
        for num in intersect:
            self.board[i][j] = num
            horizontal[i].remove(num)
            vertical[j].remove(num)
            regional[k].remove(num)
            if self.solveSudoku(horizontal, vertical, regional):
                return True
            self.board[i][j] = 0
            horizontal[i].add(num)
            vertical[j].add(num)
            regional[k].add(num)
        return False

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1

    def remove_elements(self):
        empty_cells = 50
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
                


# Example usage
generator = SudokuGenerator()
initial_state, sudoku_solution = generator.generateSudoku()
if sudoku_solution and initial_state:
    print("Full board solution:")
    for row in initial_state:
        print(row)
    print("\nInitial state:")
    for row in sudoku_solution:
        print(row)
else:
    print("No solution exists")
