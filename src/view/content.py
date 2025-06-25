import tkinter as tk
from view.open_gl_screen import OpenGLScreen

class Content:
    def __init__(self, parent, width, height, bg="#202020"):
        self.frame = tk.Frame(parent, bg=bg, width=width, height=height)
        self.frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.opengl = OpenGLScreen(self.frame, width=width, height=height)
        self.opengl.pack(expand=True, fill=tk.BOTH)

        # self.frame.after(500, self.schedule_refresh)

    def schedule_refresh(self):
        self.opengl.redraw()
        self.frame.after(2000, self.schedule_refresh)

