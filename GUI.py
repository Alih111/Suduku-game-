import tkinter as tk
import time
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Suduku")
        self.root.geometry("720x720")
        self.root.configure(bg="lightgray")
        self.canvas = tk.Canvas(self.root, width=720, height=720, bg="yellow")
    def draw_grid(self):
        # Draw horizontal lines
        for i in range(1,10):
            width=1
            if i%3==0:
                width=2
            self.canvas.create_line(80*i,0,80*i,720, width=width, fill="black")
        for i in range(1,10):
            width=1
            if i%3==0:
                width=2
            self.canvas.create_line(0,80*i,720,80*i, width=width, fill="black")
    def fillSpace(self,i,j,cell_value):
            if self.canvas:
                x = (j - 1) * 80 + 40
                y = (i - 1) * 80 + 40
                self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 20), fill="black")
    def gui(self):

        self.draw_grid()
        self.canvas.pack()
        self.root.mainloop()
g=GUI()
print(720/9)
g.fillSpace(9,9,8)
g.gui()

'''def draw_cells(canvas, cell_values,pos):
    canvas.delete("all")
    draw_grid(canvas)
    print(cell_values)
    for i in range(3):
        for j in range(3):
            cell_value = cell_values[i][j]
            color='black'
            if cell_value==0:
                color='red'
            cell_center_x = (j * 240) + 120
            cell_center_y = (i * 240) + 120
            canvas.create_text(cell_center_x, cell_center_y, text=cell_value, font=("Arial", 100), fill=color)'''
