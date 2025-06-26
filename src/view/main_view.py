# src/view/main_view.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

# Importando os utilitários de imagem
from src.view.image_utils import read_pgm, draw_image

# Importando todos os módulos de algoritmos com os nomes em inglês
from src.algorithms import (
    transformations, 
    filters, 
    algebric_operations, 
    logical_operations,
    morphism,
    histogram,
    morphological
)

# --- Configurações do Tema Escuro ---
BG_COLOR = "#2e2e2e"
FG_COLOR = "#dcdcdc"
CANVAS_BG = "#1e1e1e"
FRAME_BG = "#3e3e3e"
BUTTON_BG = "#555555"
BUTTON_FG = "#ffffff"
SELECT_BG = "#007acc"
PIXEL_GRID_BG = "#3c3c3c"

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Projeto de Processamento de Imagens")
        self.geometry("1600x900")
        self.configure(bg=BG_COLOR)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=('Arial', 10))
        style.configure("TButton", background=BUTTON_BG, foreground=BUTTON_FG, font=('Arial', 10), borderwidth=1)
        style.map("TButton", background=[('active', SELECT_BG)])
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabelframe", background=BG_COLOR, foreground=FG_COLOR, bordercolor=FG_COLOR, relief="groove")
        style.configure("TLabelframe.Label", background=FRAME_BG, foreground=FG_COLOR, font=('Arial', 11, 'bold'))
        style.configure("Pixel.TLabel", background=PIXEL_GRID_BG, foreground=FG_COLOR, font=('Courier', 10))
        style.configure("CenterPixel.TLabel", background=SELECT_BG, foreground=BUTTON_FG, font=('Courier', 10, 'bold'))

        self.image_path_1 = None
        self.image_path_2 = None
        self.image_data_1 = None
        self.image_data_2 = None
        self.result_image_data = None
        self.kernel_displays = {}
        self.pixel_grids = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=220)
        self.grid_columnconfigure(1, weight=1)

        self._create_sidebar()
        self._create_content_area()

    def _create_sidebar(self):
        sidebar_container = ttk.Frame(self, style="TFrame")
        sidebar_container.grid(row=0, column=0, sticky="ns")
        sidebar_container.grid_rowconfigure(0, weight=1)
        sidebar_container.grid_columnconfigure(0, weight=1)

        sidebar_canvas = tk.Canvas(sidebar_container, bg=FRAME_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar_container, orient="vertical", command=sidebar_canvas.yview)
        sidebar_canvas.configure(yscrollcommand=scrollbar.set)
        
        sidebar_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.sidebar_frame = ttk.Frame(sidebar_canvas, style="TFrame")
        frame_id = sidebar_canvas.create_window((0, 0), window=self.sidebar_frame, anchor="nw")

        def on_frame_configure(event):
            sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))

        def on_canvas_configure(event):
            sidebar_canvas.itemconfig(frame_id, width=event.width)

        self.sidebar_frame.bind("<Configure>", on_frame_configure)
        sidebar_canvas.bind("<Configure>", on_canvas_configure)
        
        self._populate_sidebar_widgets()

    def _populate_sidebar_widgets(self):
        file_frame = ttk.LabelFrame(self.sidebar_frame, text="Arquivo", padding=(10, 5))
        file_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(file_frame, text="Carregar Imagem 1", command=lambda: self.load_image(1)).pack(fill="x", pady=2)
        ttk.Button(file_frame, text="Carregar Imagem 2", command=lambda: self.load_image(2)).pack(fill="x", pady=2)
        ttk.Button(file_frame, text="Salvar Imagem Resultante", command=self.save_result_image).pack(fill="x", pady=(2, 0))
        
        sections = {
            "Filtros": ["Média", "Mediana", "Detecção de Bordas", "Passa Alta Básico", "Robert's", "Robert's Cruzado", "Prewitt", "Hight-boost", "Sobel"],
            "Operações Algébricas": ["Soma", "Subtração", "Multiplicação", "Divisão"],
            "Operações Lógicas": ["OR", "AND", "XOR"],
            "Morfismo": ["Iniciar Morfismo"],
            "Transformações": ["Negativo", "Gamma", "Logaritmo", "Intensidade Geral", "Faixa Dinâmica", "Linear"],
            "Histograma": ["Equalizar Histograma"],
            "Operadores Morfológicos": ["Dilatação", "Erosão", "Fechamento", "Abertura", "Hit-or-Miss", "Borda Interna", "Borda Externa", "Gradiente Morfológico", "Top-Hat", "Bottom-Hat"]
        }
        for section_title, buttons in sections.items():
            frame = ttk.LabelFrame(self.sidebar_frame, text=section_title, padding=(10, 5))
            frame.pack(fill="x", padx=10, pady=10)
            for btn_text in buttons:
                requires_two = section_title in ["Operações Algébricas", "Operações Lógicas", "Morfismo"]
                ttk.Button(frame, text=btn_text, command=lambda op=btn_text, req=requires_two: self.execute_operation(op, req)).pack(fill="x", pady=2)

    def _create_content_area(self):
        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        content_frame.grid_rowconfigure(1, weight=10)
        content_frame.grid_rowconfigure(2, weight=1) 
        
        content_frame.grid_columnconfigure(0, weight=3, uniform="group1")
        content_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        content_frame.grid_columnconfigure(2, weight=3, uniform="group1")
        content_frame.grid_columnconfigure(3, weight=3, uniform="group1")

        ttk.Label(content_frame, text="Imagem 1", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 5))
        self.canvas_1 = tk.Canvas(content_frame, bg=CANVAS_BG, relief="sunken", highlightthickness=1, highlightbackground=FG_COLOR)
        self.canvas_1.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        self._create_pixel_grid(content_frame, 'canvas_1').grid(row=2, column=0, sticky="nsew", padx=(0, 5), pady=(5,0))
        
        self._create_kernel_display(content_frame).grid(row=1, column=1, sticky="", padx=5)

        ttk.Label(content_frame, text="Imagem 2", font=("Arial", 14, "bold")).grid(row=0, column=2, pady=(0, 5))
        self.canvas_2 = tk.Canvas(content_frame, bg=CANVAS_BG, relief="sunken", highlightthickness=1, highlightbackground=FG_COLOR)
        self.canvas_2.grid(row=1, column=2, sticky="nsew", padx=5)
        self._create_pixel_grid(content_frame, 'canvas_2').grid(row=2, column=2, sticky="nsew", padx=5, pady=(5,0))

        ttk.Label(content_frame, text="Imagem Resultante", font=("Arial", 14, "bold")).grid(row=0, column=3, pady=(0, 5))
        self.canvas_result = tk.Canvas(content_frame, bg=CANVAS_BG, relief="sunken", highlightthickness=1, highlightbackground=FG_COLOR)
        self.canvas_result.grid(row=1, column=3, sticky="nsew", padx=(5, 0))
        self._create_pixel_grid(content_frame, 'canvas_result').grid(row=2, column=3, sticky="nsew", padx=(5, 0), pady=(5,0))
        
        # --- CORREÇÃO: Associa os eventos do mouse após a criação dos canvases ---
        for canvas_widget, canvas_key in [(self.canvas_1, 'canvas_1'), (self.canvas_2, 'canvas_2'), (self.canvas_result, 'canvas_result')]:
            canvas_widget.bind('<Motion>', lambda e, key=canvas_key: self._on_mouse_motion(e, key))
            canvas_widget.bind('<Leave>', self._on_mouse_leave)


    def _create_kernel_display(self, parent):
        container_frame = ttk.Frame(parent, style="TFrame")
        def create_single_kernel_panel(title, key):
            frame = ttk.LabelFrame(container_frame, text=title, padding=(10, 5))
            labels = []
            for i in range(3):
                row_labels = []
                frame.grid_rowconfigure(i, weight=1)
                frame.grid_columnconfigure(i, weight=1)
                for j in range(3):
                    label = ttk.Label(frame, text="", font=("Courier", 16, "bold"), anchor="center")
                    label.configure(background=FRAME_BG, foreground=FG_COLOR)
                    label.grid(row=i, column=j, sticky="nsew", padx=3, pady=3)
                    row_labels.append(label)
                labels.append(row_labels)
            self.kernel_displays[key] = {'frame': frame, 'labels': labels}
            return frame
        create_single_kernel_panel("Kernel", 'gx').pack(side="top", fill="x")
        create_single_kernel_panel("Kernel Gy", 'gy').pack(side="top", fill="x", pady=(10, 0))
        self.kernel_displays['gy']['frame'].pack_forget()
        return container_frame

    def _create_pixel_grid(self, parent, key):
        grid_frame = ttk.LabelFrame(parent, text="Vizinhança de Pixels", padding=(10, 5))
        labels = []
        for i in range(5):
            row_labels = []
            grid_frame.grid_rowconfigure(i, weight=1)
            grid_frame.grid_columnconfigure(i, weight=1)
            for j in range(5):
                style = "CenterPixel.TLabel" if i == 2 and j == 2 else "Pixel.TLabel"
                label = ttk.Label(grid_frame, text="-", style=style, anchor="center")
                label.grid(row=i, column=j, sticky="nsew")
                row_labels.append(label)
            labels.append(row_labels)
        self.pixel_grids[key] = labels
        return grid_frame

    def _on_mouse_motion(self, event, canvas_key):
        canvas = getattr(self, canvas_key)
        if not hasattr(canvas, 'scaling_info') or not hasattr(canvas, 'image_data'):
            return

        info = canvas.scaling_info
        
        if event.x < info['x_offset'] or event.x > info['x_offset'] + info['new_width']: return
        if event.y < info['y_offset'] or event.y > info['y_offset'] + info['new_height']: return

        original_x = int((event.x - info['x_offset']) * info['x_ratio'])
        original_y = int((event.y - info['y_offset']) * info['y_ratio'])
        
        self.update_pixel_grid('canvas_1', original_x, original_y)
        self.update_pixel_grid('canvas_2', original_x, original_y)
        self.update_pixel_grid('canvas_result', original_x, original_y)

    def _on_mouse_leave(self, event):
        self.update_pixel_grid('canvas_1', -1, -1)
        self.update_pixel_grid('canvas_2', -1, -1)
        self.update_pixel_grid('canvas_result', -1, -1)

    def update_pixel_grid(self, grid_key, center_x, center_y):
        labels = self.pixel_grids.get(grid_key)
        canvas = getattr(self, grid_key)
        if not labels or not hasattr(canvas, 'image_data'):
            for i in range(5):
                for j in range(5):
                    labels[i][j].config(text="-")
            return
            
        pixel_matrix = canvas.image_data[0]
        height = len(pixel_matrix)
        width = len(pixel_matrix[0])

        for i in range(5):
            for j in range(5):
                px = center_x + (j - 2)
                py = center_y + (i - 2)

                if 0 <= px < width and 0 <= py < height and center_x != -1:
                    value = pixel_matrix[py][px]
                    labels[i][j].config(text=str(value))
                else:
                    labels[i][j].config(text="-")

    def update_kernel_display(self, gx_matrix, gy_matrix=None):
        def update_panel(key, matrix):
            panel = self.kernel_displays.get(key)
            if not panel: return
            labels = panel['labels']
            for i in range(3):
                for j in range(3):
                    if matrix and len(matrix) == 3 and len(matrix[i]) == 3:
                        value = matrix[i][j]
                        text = f"{value:.2f}" if isinstance(value, float) else str(value)
                        labels[i][j].config(text=text)
                    else:
                        labels[i][j].config(text="")
        
        update_panel('gx', gx_matrix)
        gy_panel = self.kernel_displays['gy']['frame']
        if gy_matrix:
            update_panel('gy', gy_matrix)
            gy_panel.pack(side="top", fill="x", pady=(10, 0))
            self.kernel_displays['gx']['frame'].config(text="Kernel Gx")
        else:
            gy_panel.pack_forget()
            self.kernel_displays['gx']['frame'].config(text="Kernel")

    def load_image(self, image_number):
        filepath = filedialog.askopenfilename(title=f"Selecione a Imagem {image_number}", filetypes=[("PGM files", "*.pgm"), ("All files", "*.*")])
        if not filepath: return
        
        image_data = read_pgm(filepath)
        if image_data is None:
            messagebox.showerror("Erro de Leitura", f"Não foi possível ler o arquivo PGM:\n{filepath}", parent=self)
            return
            
        pixel_matrix, _, _, _ = image_data
        canvas_key = f'canvas_{image_number}'
        canvas = getattr(self, canvas_key)
        
        canvas.image_data = image_data
        
        if image_number == 1: self.image_data_1 = image_data
        else: self.image_data_2 = image_data
            
        draw_image(canvas, pixel_matrix)
        
        # --- CORREÇÃO: Remove a associação de eventos daqui ---

        self.canvas_result.delete("all")
        if hasattr(self.canvas_result, 'image_data'): delattr(self.canvas_result, 'image_data')
        self.update_pixel_grid('canvas_result', -1, -1)


    def save_result_image(self):
        print("Lógica para salvar imagem a ser implementada.")

    def execute_operation(self, operation_name, requires_two=False):
        if self.image_data_1 is None:
            messagebox.showwarning("Aviso", "Carregue a 'Imagem 1' primeiro.", parent=self)
            return
        if requires_two and self.image_data_2 is None:
            messagebox.showwarning("Aviso", f"A operação '{operation_name}' requer a 'Imagem 2'.", parent=self)
            return

        print(f"--- EXECUTANDO: {operation_name} ---")

        kernels = {
            "Média": ([[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]], None),
            "Detecção de Bordas": ([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], None),
            "Passa Alta Básico": ([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], None),
            "Robert's": ([[0,0,0],[0,1,0],[0,-1,0]], [[0,0,0],[0,1,-1],[0,0,0]]),
            "Robert's Cruzado": ([[0,0,0],[0,1,0],[0,0,-1]], [[0,0,0],[0,0,1],[0,-1,0]]),
            "Prewitt": ([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]), 
            "Sobel": ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
            "Hight-boost": ([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], None),
        }
        
        kernel_gx, kernel_gy = kernels.get(operation_name, (None, None))
        self.update_kernel_display(kernel_gx, kernel_gy)
        
        pixel_matrix, width, height, max_val = self.image_data_1
        result_matrix = None
        
        operations = {
            "Média": lambda: filters.apply_mean_filter(pixel_matrix),
            "Mediana": lambda: filters.apply_median_filter(pixel_matrix),
            "Detecção de Bordas": lambda: filters.apply_edge_detection_filter(pixel_matrix),
            "Passa Alta Básico": lambda: filters.apply_high_pass_basic_filter(pixel_matrix),
            "Robert's": lambda: filters.apply_roberts_filter(pixel_matrix),
            "Robert's Cruzado": lambda: filters.apply_roberts_cross_filter(pixel_matrix),
            "Prewitt": lambda: filters.apply_prewitt_filter(pixel_matrix),
            "Sobel": lambda: filters.apply_sobel_filter(pixel_matrix),
            "Negativo": lambda: transformations.apply_negative(pixel_matrix)
        }

        if operation_name in operations:
            result_matrix = operations[operation_name]()
        elif operation_name == "Hight-boost":
            factor_a = simpledialog.askfloat("Fator A", "Insira o valor de A (A > 1):", parent=self)
            if factor_a is not None:
                if factor_a > 1:
                    result_matrix = filters.apply_high_boost_filter(pixel_matrix, factor_a)
                else:
                    messagebox.showerror("Valor Inválido", "O fator A deve ser maior que 1.", parent=self)
        elif operation_name == "Soma":
            result_matrix = algebric_operations.somar_imagens(self.image_data_1[0], self.image_data_2[0])
        elif operation_name == "Subtração":
            result_matrix = algebric_operations.subtrair_imagens(self.image_data_1[0], self.image_data_2[0])
        elif operation_name == "Multiplicação":
            fator = 1.5
            result_matrix = algebric_operations.multiplicar_imagens(self.image_data_1[0], fator)
        elif operation_name == "Divisão":
            fator = 2
            result_matrix = algebric_operations.dividir_imagem(self.image_data_1[0], fator)

        if result_matrix:
            self.result_image_data = (result_matrix, width, height, max_val)
            self.canvas_result.image_data = self.result_image_data
            draw_image(self.canvas_result, result_matrix)
        else:
            self.canvas_result.delete("all")
            if hasattr(self.canvas_result, 'image_data'): delattr(self.canvas_result, 'image_data')
            self.update_pixel_grid('canvas_result', -1, -1)
