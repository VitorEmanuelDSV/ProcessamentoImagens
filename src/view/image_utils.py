# src/view/image_utils.py

import tkinter as tk

def read_pgm(filepath):
    """
    Lê um arquivo de imagem no formato PGM (P2) e retorna seus dados.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        lines = [line for line in lines if not line.strip().startswith('#')]
        
        if lines[0].strip() != 'P2':
            print("Erro: Formato de arquivo não suportado. Apenas PGM (P2) é aceito.")
            return None
        
        width, height = map(int, lines[1].strip().split())
        max_val = int(lines[2].strip())
        
        pixel_data_flat = []
        for line in lines[3:]:
            pixel_data_flat.extend(map(int, line.strip().split()))
            
        pixel_matrix = [pixel_data_flat[i*width:(i+1)*width] for i in range(height)]
            
        return (pixel_matrix, width, height, max_val)

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{filepath}'")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo PGM: {e}")
        return None

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
    y_offset = 0 # Alinha a imagem no topo

    canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=photo_image)
    
    # Armazena informações de escala e posição no próprio canvas
    # para serem usadas pelo evento de movimento do mouse.
    canvas.scaling_info = {
        'x_ratio': x_ratio,
        'y_ratio': y_ratio,
        'x_offset': x_offset,
        'y_offset': y_offset,
        'new_width': new_width,
        'new_height': new_height
    }
    
    canvas.image = photo_image
