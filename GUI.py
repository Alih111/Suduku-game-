import tkinter as tk
import time
import keyboard
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
            text_id=0
            if self.canvas:
                x = (j - 1) * 80 + 40
                y = (i - 1) * 80 + 40
                text_id=self.canvas.create_text(x, y, text=str(cell_value), font=("Arial", 20), fill="black")
            return text_id
    def getInput(self,event):
        #get click location
        x = event.x
        y = event.y
        #get click square

        for i in range(1,10):
            upperLimit = (i - 1) * 80
            downLimit = i * 80
            for j in range(1,10):
                leftLimit=(j - 1)
                rightLimit=j*80
                if x > leftLimit and x < rightLimit and y > upperLimit and y < downLimit:
                    text_id=self.fillSpace(i,j,'|')
                    pos2=j
                    pos1=i
                    break
        self.canvas.update()
        #get variable polling
        key= keyboard.read_event()
        while True:
                if key.name.isdigit():
                    self.canvas.delete(text_id)
                    a=self.fillSpace(pos1,pos2,key.name)
                    break
                else:
                    print("wrong input")
                    key = keyboard.read_event()

        self.canvas.update()
    def gui(self):

        self.draw_grid()
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.getInput)
        self.root.mainloop()
g=GUI()
print(720/9)
g.gui()

