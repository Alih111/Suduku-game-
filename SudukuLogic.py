class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def solve_sudoku(self):
        # Convert the current board state to a CSP representation
        csp_representation = self.convert_to_csp()

        # Perform backtracking search with arc consistency
        solution = self.backtrack_search(csp_representation)

        return solution

    def convert_to_csp(self):
        csp_representation = {}
        for i in range(9):
            for j in range(9):
                value = self.board[i][j]
                if value:
                    csp_representation[(i, j)] = int(value)
                else:
                    csp_representation[(i, j)] = set(range(1, 10))
        return csp_representation

    def backtrack_search(self, csp_representation):
        if self.is_complete(csp_representation):
            return csp_representation

        # Select an unassigned variable
        var = self.select_unassigned_variable(csp_representation)

        # Try assigning a value to the variable and recursively search
        for value in csp_representation[var]:
            if self.is_consistent(csp_representation, var, value):
                csp_representation[var] = value
                result = self.backtrack_search(csp_representation)
                if result:
                    return result
            csp_representation[var] = set(range(1, 10))  # Undo assignment if unsuccessful
        return None

    def is_complete(self, csp_representation):
        return all(isinstance(val, int) for val in csp_representation.values())

    def select_unassigned_variable(self, csp_representation):
        for var, value in csp_representation.items():
            if isinstance(value, set):
                return var
        return None

    def is_consistent(self, csp_representation, var, value):
        # Check row and column consistency
        for i in range(9):
            if i != var[0] and csp_representation[(i, var[1])] == value:
                return False
            if i != var[1] and csp_representation[(var[0], i)] == value:
                return False

        # Check 3x3 subgrid consistency
        start_row, start_col = var[0] - var[0] % 3, var[1] - var[1] % 3
        for i in range(3):
            for j in range(3):
                row = start_row + i
                col = start_col + j
                if (row, col) != var and csp_representation[(row, col)] == value:
                    return False
        return True
