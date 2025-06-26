# src/view/image_utils.py

import tkinter as tk

def read_pgm(filepath):
    """
    Lê um arquivo de imagem no formato PGM (P2) e retorna seus dados.

    Args:
        filepath (str): O caminho para o arquivo PGM.

    Returns:
        tuple: Uma tupla contendo (matriz_de_pixels, largura, altura, valor_maximo)
               ou None se o arquivo for inválido ou não encontrado.
    """
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Ignora linhas de comentário
        lines = [line for line in lines if not line.strip().startswith('#')]
        
        # Verifica o "número mágico" (deve ser P2)
        if lines[0].strip() != 'P2':
            print("Erro: Formato de arquivo não suportado. Apenas PGM (P2) é aceito.")
            return None
        
        # Lê largura e altura
        width, height = map(int, lines[1].strip().split())
        
        # Lê o valor máximo de cinza
        max_val = int(lines[2].strip())
        
        # Lê os dados dos pixels
        pixel_data_flat = []
        for line in lines[3:]:
            pixel_data_flat.extend(map(int, line.strip().split()))
            
        # Constrói a matriz 2D de pixels
        pixel_matrix = []
        for i in range(height):
            start = i * width
            end = start + width
            pixel_matrix.append(pixel_data_flat[start:end])
            
        return (pixel_matrix, width, height, max_val)

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{filepath}'")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo PGM: {e}")
        return None

def draw_image(canvas, pixel_matrix):
    """
    Desenha uma matriz de pixels em um canvas do Tkinter.

    Args:
        canvas (tk.Canvas): O widget do canvas onde a imagem será desenhada.
        pixel_matrix (list): Uma lista de listas representando os pixels da imagem.
    """
    if not pixel_matrix:
        return
        
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    
    # Limpa o canvas antes de desenhar
    canvas.delete("all")

    # Cria um objeto PhotoImage. Esta é a maneira mais eficiente de desenhar pixel a pixel.
    photo_image = tk.PhotoImage(width=width, height=height)
    
    # Monta a string de dados da imagem no formato que o PhotoImage entende.
    # Cada pixel é um grupo de cores. Ex: "{#RRGGBB #RRGGBB ...}"
    # O f-string '{p:02x}' formata um número para hexadecimal com 2 dígitos.
    image_data_string = " ".join(
        "{" + " ".join(f"#{p:02x}{p:02x}{p:02x}" for p in row) + "}" 
        for row in pixel_matrix
    )
    
    photo_image.put(image_data_string)

    # Coloca a imagem no canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
    
    # IMPORTANTE: Mantém uma referência à imagem para evitar que ela seja
    # coletada pelo garbage collector do Python, o que a faria desaparecer.
    canvas.image = photo_image
