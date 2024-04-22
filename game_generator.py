from random import randrange
from random import shuffle
class SudokuGenerator:
    def generateSudoku(self):
        board = [[0] * 9 for _ in range(9)]

        horizontal = [set(range(1, 10)) for _ in range(9)]
        vertical = [set(range(1, 10)) for _ in range(9)]
        regional = [set(range(1, 10)) for _ in range(9)]

        if self.solveSudoku(board, horizontal, vertical, regional):
            solved_board = [row[:] for row in board]
            self.remove_elements(board)
            return solved_board, board
        else:
            return None, None

    def not_full(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return True
        return False
    def is_valid_move(self,board, row, col, num):
        # Check if the number already exists in the row
        if num in board[row]:
            return False
    
        # Check if the number already exists in the column
        if num in [board[i][col] for i in range(9)]:
            return False
    
        # Check if the number already exists in the 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
            
        return True
    def find_empty_cell(self,board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def count_solutions(self,board):
        count = [0]

        def solve(board):
            empty_cell = self.find_empty_cell(board)
            if not empty_cell:
                count[0] += 1
                return
        
            row, col = empty_cell
            for num in range(1, 10):
                if self.is_valid_move(board, row, col, num):
                    board[row][col] = num
                    solve(board)
                    board[row][col] = 0  # Backtrack

        solve(board)
        return count[0]

    def solveSudoku(self, board, horizontal, vertical, regional):
        if not self.not_full(board):
            return True

        i, j = self.find_empty_location(board)
        k = i // 3 * 3 + j // 3

        intersect = horizontal[i] & vertical[j] & regional[k]
        intersect = list(intersect)
        shuffle(intersect)
        for num in intersect:
            board[i][j] = num
            horizontal[i].remove(num)
            vertical[j].remove(num)
            regional[k].remove(num)
            if self.solveSudoku(board, horizontal, vertical, regional):
                return True
            board[i][j] = 0
            horizontal[i].add(num)
            vertical[j].add(num)
            regional[k].add(num)
        return False

    def find_empty_location(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return -1, -1

    def remove_elements(self, board):
        empty_cells = 30
        while empty_cells > 0:
            i, j = randrange(9), randrange(9)
            while board[i][j] == 0:
                i, j = randrange(9), randrange(9)
            temp = board[i][j]
            board[i][j] = 0
            
            temp_board = [row[:] for row in board]
            if self.count_solutions(temp_board) == 1:
                empty_cells -= 1
            else:
                board[i][j] = temp
                

    def has_unique_solution(self, board):
        horizontal = [set(range(1, 10)) for _ in range(9)]
        vertical = [set(range(1, 10)) for _ in range(9)]
        regional = [set(range(1, 10)) for _ in range(9)]
        return self.solveSudoku(board, horizontal, vertical, regional)

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
