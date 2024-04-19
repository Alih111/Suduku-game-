import tkinter as tk
import time
import keyboard
from SudukuLogic import SudokuSolver

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.root.geometry("720x760")
        self.root.configure(bg="lightgray")

        self.canvas = tk.Canvas(self.root, width=720, height=720, bg="white")
        self.canvas.pack(pady=10)

        self.button_frame = tk.Frame(self.root, bg="lightgray")
        self.button_frame.pack()

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve_sudoku)
        self.solve_button.pack(side=tk.LEFT, padx=10, pady=10)


        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solver = SudokuSolver(self.board)

    def draw_grid(self):
        # Draw horizontal lines
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

    def fill_space(self, i, j, cell_value):
        text_id = 0
        if self.canvas:
            x = (j - 1) * 80 + 40
            y = (i - 1) * 80 + 40
            text_id = self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 20), fill="black")
        return text_id

    def get_input(self, event):
        # Get click location
        x = event.x
        y = event.y
        # Get click square
        for i in range(1, 10):
            upper_limit = (i - 1) * 80
            down_limit = i * 80
            for j in range(1, 10):
                left_limit = (j - 1) * 80
                right_limit = j * 80
                if x > left_limit and x < right_limit and y > upper_limit and y < down_limit:
                    text_id = self.fill_space(i, j, '|')
                    pos2 = j
                    pos1 = i
                    break
        self.canvas.update()
        # Get variable polling
        key = keyboard.read_event()
        while True:
            if key.name.isdigit():
                self.canvas.delete(text_id)
                self.fill_space(pos1, pos2, key.name)
                self.board[pos1 - 1][pos2 - 1] = int(key.name)
                break
            else:
                print("wrong input")
                key = keyboard.read_event()

    def solve_sudoku(self):
        solution = self.solver.solve_sudoku()
        if solution:
            self.update_gui(solution)
        else:
            print("No solution found.")

    def update_gui(self, solution):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = solution[(i, j)]
                self.canvas.delete("cell" + str(i) + str(j))
                self.fill_space(i+1, j+1, self.board[i][j])

    def gui(self):
        self.draw_grid()
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.get_input)
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_sudoku)
        solve_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.root.mainloop()


# Example usage:
gui = GUI()
gui.gui()
