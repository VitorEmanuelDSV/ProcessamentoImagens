import tkinter as tk

class MainWindow:
    def __init__(self, width=1600, height=900):
        self.root = tk.Tk()
        self.root.title("Computação Gráfica")
        self.root.geometry(f"{width}x{height}")
        self.width = width
        self.height = height

    def run(self):
        self.root.mainloop()
