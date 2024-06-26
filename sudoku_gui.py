import tkinter as tk
import time
import keyboard
from SudukuLogic import SudokuSolver
from game_generator import SudokuGenerator
class GUI:
    def __init__(self ,mode=1):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.root.geometry("800x720")
        self.root.configure(bg="lightgray")
        self.loc_id=[[0] * 9 for _ in range(9)]
        self.canvas = tk.Canvas(self.root, width=720, height=720, bg="white")
        self.canvas.pack(pady=10)
        self.button_frame = tk.Frame(self.root, bg="lightgray")
        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve_sudoku)
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solved_board = [[0 for _ in range(9)] for _ in range(9)]
        self.userIsEnteringThePuzzle=False
        # self.solver = SudokuSolver(self.board)
        if mode == 1:
            self.generate_initial_state()
        elif mode == 2:
            self.get_user_board()
    def draw_grid(self):
        # Draw horizontal lines
        self.canvas.create_line(2, 0, 2, 720, width=3, fill="black")
        self.canvas.create_line(0, 2, 720, 2, width=3, fill="black")
        for i in range(1, 10):
            width = 1
            if i % 3 == 0:
                width = 2
            self.canvas.create_line(80 * i, 0, 80 * i, 720, width=width, fill="black")
        for i in range(1, 10):
            width = 1
            if i % 3 == 0:
                width = 2
            self.canvas.create_line(0, 80 * i, 720, 80 * i, width=width, fill="black")

    def fill_space(self, i, j, cell_value, color="red"):
        text_id = 0
        if self.canvas:
            x = (j - 1) * 80 + 40
            y = (i - 1) * 80 + 40
            if self.loc_id[i-1][j-1]==0:
                text_id = self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 20), fill=color)
                self.loc_id[i-1][j-1]=text_id
            else:
                self.canvas.delete(self.loc_id[i-1][j-1])
                text_id = self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 20), fill=color)
                self.loc_id[i-1][j-1]= text_id
        return text_id

    def get_input(self, event):
        # Get click location
        x = event.x
        y = event.y
        flag=False
        # Get click square
        for i in range(1, 10):
            upper_limit = (i - 1) * 80
            down_limit = i * 80
            for j in range(1, 10):
                left_limit = (j - 1) * 80
                right_limit = j * 80
                if x > left_limit and x < right_limit and y > upper_limit and y < down_limit:
                    text_id=self.fill_space(i, j, '|')
                    pos2 = j
                    pos1 = i
                    flag=True
                    break
        wrongInput=False
        text_id2=0
        if flag:
            self.canvas.update()
            # Get variable polling
            key = keyboard.read_event()
            if key.name.isdigit() and int(key.name) > 0:
                text_id2=self.fill_space(pos1, pos2, key.name)
                self.board[pos1 - 1][pos2 - 1] = int(key.name)
            else:
                print("wrong input")
                self.canvas.delete(text_id)
                wrongInput=True
            if  not wrongInput:#check if user input is possible for a suduku puzzle
                solver = SudokuSolver(self.board)
                if solver.AC_3():
                    pass
                else:
                    self.canvas.delete(text_id2)
                    self.board[pos1-1][pos2-1]=0
                    self.errorWindow("this is not a suduku puzzle")
                del(solver)
            self.canvas.update()


    def solve_sudoku(self):
        k=0
        self.canvas.unbind("<Button-1>")
        for i in range(9):
            for j in range(9):
                if self.board[i][j] !=0:
                    k+=1
        if k >= 7:
            solver = SudokuSolver(self.board)
            solution = solver.solve_sudoku()
            if solution:
                self.update_gui(solution)
            else:
                self.errorWindow("No solution found.")
        key = keyboard.read_event()
        if self.userIsEnteringThePuzzle:#check if user input is possible for a suduku puzzle
            solver = SudokuSolver(self.board)
            
            if solver.AC_3():
                pass
            
            else:
                error_window = tk.Tk()
                error_window.title("wrong input")
                error_window.geometry("300x300")
                error_label = tk.Label(error_window, text="this is not a suduku puzzle", foreground="blue", font=("Arial", 12))
                error_label.pack(padx=20, pady=20)
                error_window.mainloop()
            del(solver)


    def solve_sudoku(self):
        self.canvas.unbind("<Button-1>")
        solver = SudokuSolver(self.board)
        k=0
        for i in range (9):
            for j in range(9):
                if self.board[i][j]!=0:
                    k+=1
       # for row in self.board:
        #    print(row)
        
        
        if k >=7:
            count = solver.count_possible_solutions(self.board)
            solution = solver.solve_sudoku()
            self.canvas.bind("<Button-1>", self.get_input)
        
            if solution:
                self.update_gui(solution)
                self.errorWindow(f"the number of possible solution is {count}")  
            else:
                self.errorWindow("no solution")
              
        else:
            self.errorWindow("enter at least 7 clues")
        
    def errorWindow(self,text):
        error_window = tk.Tk()
        error_window.title("wrong input")
        error_window.geometry("300x200")
        error_label = tk.Label(error_window, text=text, foreground="blue",
                               font=("Arial", 12))
        error_label.pack(padx=20, pady=20)
        error_window.mainloop()
    def update_gui(self, solution):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != solution[i][j]:
                    self.board[i][j] = solution[i][j]
                    self.canvas.delete("cell" + str(i) + str(j))
                    self.fill_space(i+1, j+1, self.board[i][j],"blue")
    def update_generate_gui(self, solution):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = solution[i][j]
                if self.board[i][j] != 0:
                    self.canvas.delete("cell" + str(i) + str(j))
                    self.fill_space(i+1, j+1, self.board[i][j],color='black')
    def gui(self):
        self.draw_grid()
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.get_input)
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.pack(side=tk.TOP, padx=10, pady=10)
        self.root.mainloop()
    def is_initial_state_valid(self):
        # Check if the initial state contains only digits from 1 to 9
        for row in self.board:
            for cell in row:
                if not isinstance(cell, int) or cell < 1 or cell > 9:
                    return False
        return True
    def generate_initial_state(self):
        generator = SudokuGenerator()
        self.solved_board ,self.board = generator.generateSudoku()
        self.update_generate_gui(self.board)
    def get_user_board(self):
        self.userIsEnteringThePuzzle = True


