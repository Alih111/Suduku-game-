
class SudokuSolver:
    def __init__(self, board):
        self.board = board
        print("\nInitial state:")
        for row in self.board:
            print(row)

    def solve_sudoku(self):
        # Convert the current board state to a CSP representation
        csp = self.convert_to_csp()

        # Perform backtracking search with arc consistency
        solution = self.backtrack_search(csp)

        return solution

    def convert_to_csp(self):
        csp = []
        for i in range(9):
            row_values = []
            for j in range(9):
                value = self.board[i][j]
                if value:
                    row_values.append(int(value))
                else:
                    row_values.append(set(range(1, 10)))
            csp.append(row_values)
        return csp

    def calculate_domain(self, row, col):
        domain = set(range(1, 10))
        for i in range(9):
            # Exclude values already present in the same row
            if self.board[row][i] != 0:
                domain.discard(self.board[row][i])
            # Exclude values already present in the same column
            if self.board[i][col] != 0:
                domain.discard(self.board[i][col])
        # Exclude values already present in the same block
        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] != 0:
                    domain.discard(self.board[start_row + i][start_col + j])
        return domain

    def backtrack_search(self, csp):
        if self.is_complete(csp):
            return csp

        # Select an unassigned variable
        var = self.select_unassigned_variable(csp)

        # Retrieve the domain of the selected variable
        domain = self.calculate_domain(var[0], var[1])

        # Print domain of the selected variable (empty cell)
        print(f"Domain of cell ({var[0]}, {var[1]}): {domain}")

        # Try assigning a value to the variable and recursively search
        for value in domain:
            if self.is_consistent(csp, var, value):
                csp[var[0]][var[1]] = value
                result = self.backtrack_search(csp)
                if result:
                    return result
            csp[var[0]][var[1]] = set(range(1, 10))  # Undo assignment if unsuccessful
        return None

    def is_complete(self, csp):
        return all(isinstance(val, int) for row in csp for val in row)

    def select_unassigned_variable(self, csp):
        for i in range(9):
            for j in range(9):
                if isinstance(csp[i][j], set):
                    return i, j
        return None

    def is_consistent(self, csp, var, value):
        # Check row and column consistency
        for i in range(9):
            if i != var[0] and csp[i][var[1]] == value:
                return False
            if i != var[1] and csp[var[0]][i] == value:
                return False

        # Check 3x3 subgrid consistency
        start_row, start_col = var[0] - var[0] % 3, var[1] - var[1] % 3
        for i in range(3):
            for j in range(3):
                row = start_row + i
                col = start_col + j
                if (row, col) != var and csp[row][col] == value:
                    return False
        return True

    def count_possible_solutions(self, board):
        # Convert the current board state to a CSP representation
        self.board = board
        csp = self.convert_to_csp()

        # Initialize a counter for solutions
        self.solution_count = 0

        # Perform backtracking search with arc consistency to count solutions
        self.backtrack_count(csp)

        return self.solution_count

    def backtrack_count(self, csp):
        if self.is_complete(csp):
            # If a solution is found, increment the solution count
            self.solution_count += 1
            return

        # Select an unassigned variable
        var = self.select_unassigned_variable(csp)

        # Try assigning a value to the variable and recursively search
        for value in csp[var[0]][var[1]]:
            if self.is_consistent(csp, var, value):
                csp[var[0]][var[1]] = value
                self.backtrack_count(csp)
            csp[var[0]][var[1]] = set(range(1, 10))  # Undo assignment if unsuccessful
