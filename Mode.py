import tkinter as tk
from sudoku_gui import GUI

class ModelSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Model Selector")
        self.root.geometry("300x200")
        self.root.configure(bg="lightgray")

        self.label = tk.Label(self.root, text="Choose a Model:", font=("Arial", 14), bg="lightgray")
        self.label.pack(pady=10)

        self.model1_button = tk.Button(self.root, text="Model 1", command=self.run_model1_gui)
        self.model1_button.pack(pady=5)

        self.model2_button = tk.Button(self.root, text="Model 2", command=self.run_model2_gui)
        self.model2_button.pack(pady=5)

    def run_model1_gui(self):
        self.root.destroy()
        gui = GUI()
        gui.gui()

    def run_model2_gui(self):
        # Add code to run model 2 GUI here
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    selector = ModelSelector()
    selector.run()
