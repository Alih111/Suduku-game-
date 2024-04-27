
import time
class SudokuSolver:
    def __init__(self, board):
        self.board=board
        self.variables = []
        self.arcs = []
        self.domains = {}
        self.initVariables()
        self.initArcs()
        self.initDomain()
    def initVariables(self):#craete variables for the whole board
        for i in range(9):
            for j in range(9):
                self.variables.append((i,j))
    def initArcs(self):#initalize arcs for the whole board
        for i in range(9):# row arcs
            for j in range(8):
                for k in range(j + 1, 9):
                    self.arcs.append(((i, j), (i, k)))
        for i in range(9):# column arcs
            for j in range(8):
                for k in range(j + 1, 9):
                    self.arcs.append(((j,i), (k,i)))
        # box arcs
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                box_cells = [(row + i, col + j) for i in range(3) for j in range(3)]#get all the cells in the box
                for i, cell1 in enumerate(box_cells):
                    for cell2 in box_cells[i + 1:]:
                        self.arcs.append((cell1, cell2))
    def initDomain(self):# initialize domain for each variabe
        for variable in self.variables:
            if self.board[variable[0]][variable[1]]==0:
                self.domains[variable] = set(range(1, 10))
            else:
                self.domains[variable] = self.board[variable[0]][variable[1]]

    def revise(self, x,steps):
        
        revised = False
        if isinstance(self.domains[x[0]], int):
            value = self.domains[x[0]]
            if isinstance(self.domains[x[1]], set) and value in self.domains[x[1]]:
                print("Step : "+str(steps))
                print(f"Arc : {x[0]} -> {x[1]}")
                print(f"Domains : {self.domains[x[0]]} -> {self.domains[x[1]]}")
                print(f"Remove ({value}) from {x[1]}")
                self.domains[x[1]].remove(value)
                print(f"New domain : {self.domains[x[1]]}")   
                revised = True
            elif isinstance(self.domains[x[1]], int) and value == self.domains[x[1]]:
                print("Step : "+str(steps))
                print(f"Arc : {x[0]} -> {x[1]}")
                print(f"Domains : {self.domains[x[0]]} -> {self.domains[x[1]]}")
                print(f"Remove ({value}) from {x[1]}")
                print("New domain : {}")
                revised = True
    
        return revised

    def AC_3(self):
        queue = set(self.arcs)
        steps = 1
        while queue:
            arc = queue.pop()
            if self.revise(arc,steps):
                
                if isinstance(self.domains[arc[1]], int) and self.domains[arc[0]] == self.domains[arc[1]] or (isinstance(self.domains[arc[1]],set)and len(self.domains[arc[1]])==0) :
                    return False
                for xl, xk in self.arcs:
                    if xl != arc[0] and xk == arc[1]:
                        queue.add((arc[1],xl))
            steps = steps+1            
        return True
    
    def solve_sudoku(self):
        # Perform backtracking search with arc consistency
        if self.AC_3():
            solution = self.backtrack_search()
            if solution is None:
                return None
            value = [[0 for _ in range(9)] for _ in range(9)]
            for i in range(9):
                for j in range(9):
                    value[i][j] = self.domains[(i, j)]
            return value
        else:
            return None

    def backtrack_search(self):
        if self.is_complete():
            return self.domains
        # Select an unassigned variable
        var = self.select_unassigned_variable()
        if var is None:
            
            return None  # No solution found
        # Retrieve the domain of the selected variable
        domain = self.domains[var].copy()
        # Try assigning a value to the variable and recursively search
        for value in list(domain):
            # Assign the value to the variable
            self.domains[var] = value
            if self.isConsistent(var) :
                result = self.backtrack_search()
                if result is not None:
                    return result  # Solution found
            self.domains[var] = domain  # Undo assignment if unsuccessful
        return None
    def isConsistent(self,variable):
        arcs=self.arcs.copy()
        for arc in arcs:
            if arc[0]==variable and not isinstance(self.domains[arc[1]],set) and self.domains[variable]== self.domains[arc[1]] :
               return False
            if arc[1]==variable and not isinstance(self.domains[arc[0]],set)  and self.domains[variable] == self.domains[arc[0]]:
                return False
        return True

    def is_complete(self):
        i=0
        for domain in self.domains.values():
            i+=1
            if not isinstance(domain,int):
                return False
        return True
    def select_unassigned_variable(self):#changed
        min_domain_size = 10  # Initialize with a high value
        selected_variable = None
        for variable in self.variables:
            if isinstance(self.domains[variable],set):
                domain_size = len(self.domains[variable])
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    selected_variable = variable
        return selected_variable



    def count_possible_solutions(self, board):
        # Convert the current board state to a CSP representation
        self.board = board
        self.initVariables()
        self.initArcs()
        self.initDomain()
        # Initialize a counter for solutions
        self.solution_count = 0

        # Perform backtracking search with arc consistency to count solutions
        self.backtrack_count()

        return self.solution_count

    def backtrack_count(self):
        if self.is_complete():

            self.solution_count += 1
            return
        # Select an unassigned variable
        var = self.select_unassigned_variable()
        if var is None:
            return None  # No solution found
        # Retrieve the domain of the selected variable
        domain = self.domains[var].copy()
        # Try assigning a value to the variable and recursively search
        for value in list(domain):
            # Assign the value to the variable
            self.domains[var] = value
            if self.isConsistent(var) :
                result = self.backtrack_count()
            self.domains[var] = domain  # Undo assignment if unsuccessful

