# src/view/image_utils.py

import tkinter as tk
from tkinter import messagebox

def _read_pbm_p1(lines):
    """Lê os dados de um arquivo PBM (P1) e os converte para escala de cinza."""
    width, height = map(int, lines[1].strip().split())
    pixel_data_flat = []
    for line in lines[2:]:
        pixel_data_flat.extend(map(int, line.strip().split()))

    pixel_matrix_01 = [pixel_data_flat[i*width:(i+1)*width] for i in range(height)]
    pixel_matrix_255 = [[(1 - pixel) * 255 for pixel in row] for row in pixel_matrix_01]
    
    return (pixel_matrix_255, width, height, 255)

def _read_pgm_p2(lines):
    """Lê os dados de um arquivo PGM (P2)."""
    width, height = map(int, lines[1].strip().split())
    max_val = int(lines[2].strip())
    pixel_data_flat = []
    for line in lines[3:]:
        pixel_data_flat.extend(map(int, line.strip().split()))
            
    pixel_matrix = [pixel_data_flat[i*width:(i+1)*width] for i in range(height)]
            
    return (pixel_matrix, width, height, max_val)

def read_pgm(filepath):
    """
    Lê um arquivo de imagem no formato Netpbm (PGM ou PBM) e retorna seus dados.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        
        magic_number = lines[0].strip()
        
        if magic_number == 'P1':
            return _read_pbm_p1(lines)
        elif magic_number == 'P2':
            return _read_pgm_p2(lines)
        else:
            messagebox.showerror("Formato Inválido", f"Formato de arquivo não suportado: '{magic_number}'. Apenas PGM (P2) e PBM (P1) são aceitos.")
            return None

    except FileNotFoundError:
        messagebox.showerror("Erro de Arquivo", f"Arquivo não encontrado em:\n'{filepath}'")
        return None
    except Exception as e:
        messagebox.showerror("Erro de Leitura", f"Ocorreu um erro ao ler o arquivo:\n{e}")
        return None

def write_pgm(filepath, image_data):
    """
    Escreve uma matriz de pixels em um arquivo no formato PGM (P2).

    Args:
        filepath (str): O caminho para salvar o arquivo.
        image_data (tuple): Tupla contendo (matriz_de_pixels, largura, altura, valor_maximo).
    """
    try:
        pixel_matrix, width, height, max_val = image_data
        
        with open(filepath, 'w') as f:
            # Escreve o cabeçalho do PGM
            f.write("P2\n")
            f.write(f"{width} {height}\n")
            f.write(f"{max_val}\n")
            
            # Escreve os dados dos pixels
            for row in pixel_matrix:
                f.write(" ".join(map(str, row)) + "\n")
        
        messagebox.showinfo("Sucesso", f"Imagem salva com sucesso em:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar a imagem:\n{e}")


def draw_image(canvas, pixel_matrix):
    """
    Desenha uma matriz de pixels em um canvas, redimensionando-a para caber
    no espaço disponível, mantendo a proporção e alinhando ao topo.
    """
    if not pixel_matrix or not pixel_matrix[0]:
        canvas.delete("all")
        return
        
    canvas.delete("all")
    canvas.update_idletasks()
    
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    if canvas_width <= 1 or canvas_height <= 1:
        return

    image_height = len(pixel_matrix)
    image_width = len(pixel_matrix[0])

    img_aspect = image_width / image_height
    canvas_aspect = canvas_width / canvas_height

    if img_aspect > canvas_aspect:
        new_width = canvas_width
        new_height = int(new_width / img_aspect)
    else:
        new_height = canvas_height
        new_width = int(new_height * img_aspect)

    if new_width == 0 or new_height == 0: return

    scaled_pixel_matrix = [[0] * new_width for _ in range(new_height)]
    x_ratio = image_width / new_width
    y_ratio = image_height / new_height

    for y in range(new_height):
        for x in range(new_width):
            px = int(x * x_ratio)
            py = int(y * y_ratio)
            scaled_pixel_matrix[y][x] = pixel_matrix[py][px]

    photo_image = tk.PhotoImage(width=new_width, height=new_height)
    
    image_data_string = " ".join(
        "{" + " ".join(f"#{p:02x}{p:02x}{p:02x}" for p in row) + "}" 
        for row in scaled_pixel_matrix
    )
    
    photo_image.put(image_data_string)

    x_offset = (canvas_width - new_width) // 2
    y_offset = 0

    canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=photo_image)
    
    canvas.scaling_info = {
        'x_ratio': x_ratio,
        'y_ratio': y_ratio,
        'x_offset': x_offset,
        'y_offset': y_offset,
        'new_width': new_width,
        'new_height': new_height
    }
    
    canvas.image = photo_image
