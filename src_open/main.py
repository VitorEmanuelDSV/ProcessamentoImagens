from view.main_window import MainWindow
from view.content import Content
import tkinter as tk

if __name__ == "__main__":
    width = 1280
    height = 720

    app = MainWindow(width, height)

    # 1. Criar Main Frame (vai abrigar Content)
    main_frame = tk.Frame(app.root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 2. Dentro do main_frame criar Content
    content = Content(main_frame, width, height)

    app.run()