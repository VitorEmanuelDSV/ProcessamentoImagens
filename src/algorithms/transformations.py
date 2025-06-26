# src/algorithms/transformations.py

import math

def find_min_max(pixel_matrix):
    """Encontra os valores mínimo e máximo de pixels em uma matriz."""
    min_val = 255
    max_val = 0
    for row in pixel_matrix:
        for pixel in row:
            if pixel < min_val:
                min_val = pixel
            if pixel > max_val:
                max_val = pixel
    return min_val, max_val

def apply_negative(pixel_matrix):
    """
    Calcula o negativo de uma imagem.
    Aplica a fórmula S = 255 - r para cada pixel.
    """
    if not pixel_matrix:
        return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[255 - pixel for pixel in row] for row in pixel_matrix]
    return output_matrix

def apply_gamma_correction(pixel_matrix, gamma, c=1):
    """
    Aplica a correção gamma em uma imagem.
    Fórmula: S = c * (r^gamma). Normaliza o pixel para [0, 1] antes de aplicar.
    """
    if not pixel_matrix:
        return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            normalized_pixel = pixel_matrix[y][x] / 255.0
            corrected_pixel = c * math.pow(normalized_pixel, gamma)
            final_pixel = int(round(corrected_pixel * 255.0))
            if final_pixel > 255: final_pixel = 255
            if final_pixel < 0: final_pixel = 0
            output_matrix[y][x] = final_pixel
    return output_matrix

def apply_logarithmic(pixel_matrix, max_pixel_value):
    """
    Aplica a transformação logarítmica.
    Fórmula: S = c * log(1 + r), onde c = 255 / log(1 + max_val).
    """
    if not pixel_matrix:
        return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    c = 255 / math.log(1 + max_pixel_value)
    for y in range(height):
        for x in range(width):
            r = pixel_matrix[y][x]
            s = c * math.log(1 + r)
            output_matrix[y][x] = int(round(s))
    return output_matrix

def apply_sigmoid(pixel_matrix, w_center, sigma_width):
    """
    Aplica a função de transferência de intensidade geral (Sigmoide).
    Fórmula: S = 255 / (1 + e^(-(r - w) / sigma))
    """
    if not pixel_matrix:
        return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    if sigma_width == 0: sigma_width = 1.0
    for y in range(height):
        for x in range(width):
            r = pixel_matrix[y][x]
            try:
                exponent = -(r - w_center) / sigma_width
                s = 255 / (1 + math.exp(exponent))
                output_matrix[y][x] = int(round(s))
            except OverflowError:
                output_matrix[y][x] = 255 if exponent < 0 else 0
    return output_matrix

def apply_dynamic_range(pixel_matrix):
    """
    Aplica a transformação de faixa dinâmica (alongamento de contraste).
    Fórmula: S = (r - r_min) * 255 / (r_max - r_min)
    """
    if not pixel_matrix:
        return None
    
    r_min, r_max = find_min_max(pixel_matrix)
    if r_max == r_min:
        return pixel_matrix # Evita divisão por zero se a imagem for de cor única
        
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    
    scale = 255.0 / (r_max - r_min)

    for y in range(height):
        for x in range(width):
            r = pixel_matrix[y][x]
            s = (r - r_min) * scale
            output_matrix[y][x] = int(round(s))
            
    return output_matrix

def apply_linear_transfer(pixel_matrix, r1, s1, r2, s2):
    """
    Aplica uma transformação linear por partes (piecewise-linear).
    """
    if not pixel_matrix:
        return None

    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    
    # Pré-calcula as inclinações para cada segmento da função
    slope1 = s1 / r1 if r1 != 0 else 0
    slope2 = (s2 - s1) / (r2 - r1) if (r2 - r1) != 0 else 0
    slope3 = (255 - s2) / (255 - r2) if (255 - r2) != 0 else 0

    for y in range(height):
        for x in range(width):
            r = pixel_matrix[y][x]
            s = 0
            if r < r1:
                s = slope1 * r
            elif r1 <= r <= r2:
                s = slope2 * (r - r1) + s1
            else:
                s = slope3 * (r - r2) + s2
            
            if s > 255: s = 255
            if s < 0: s = 0
            output_matrix[y][x] = int(round(s))
            
    return output_matrix
