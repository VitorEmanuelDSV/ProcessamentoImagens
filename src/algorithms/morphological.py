# src/algorithms/morphological.py

from src.algorithms import matrix_utils

def apply_dilation(pixel_matrix, kernel_size=3):
    """
    Aplica a operação de dilatação em uma imagem em escala de cinza.
    A dilatação substitui o valor de um pixel pelo valor MÁXIMO
    na sua vizinhança, definida pelo elemento estruturante.
    Expande as regiões claras.
    """
    if not pixel_matrix:
        return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    offset = kernel_size // 2
    for y in range(height):
        for x in range(width):
            max_val = 0
            for i in range(-offset, offset + 1):
                for j in range(-offset, offset + 1):
                    ny, nx = y + i, x + j
                    if 0 <= ny < height and 0 <= nx < width:
                        pixel_value = pixel_matrix[ny][nx]
                        if pixel_value > max_val:
                            max_val = pixel_value
            output_matrix[y][x] = max_val
    return output_matrix

def apply_erosion(pixel_matrix, kernel_size=3):
    """
    Aplica a operação de erosão em uma imagem em escala de cinza.
    A erosão substitui o valor de um pixel pelo valor MÍNIMO
    na sua vizinhança, definida pelo elemento estruturante.
    Expande as regiões escuras (encolhe as claras).
    """
    if not pixel_matrix:
        return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    offset = kernel_size // 2
    for y in range(height):
        for x in range(width):
            min_val = 255
            for i in range(-offset, offset + 1):
                for j in range(-offset, offset + 1):
                    ny, nx = y + i, x + j
                    if 0 <= ny < height and 0 <= nx < width:
                        pixel_value = pixel_matrix[ny][nx]
                        if pixel_value < min_val:
                            min_val = pixel_value
            output_matrix[y][x] = min_val
    return output_matrix

def apply_opening(pixel_matrix, kernel_size=3):
    """Aplica a operação de abertura morfológica (Erosão -> Dilatação)."""
    eroded_image = apply_erosion(pixel_matrix, kernel_size)
    opened_image = apply_dilation(eroded_image, kernel_size)
    return opened_image

def apply_closing(pixel_matrix, kernel_size=3):
    """Aplica a operação de fechamento morfológico (Dilatação -> Erosão)."""
    dilated_image = apply_dilation(pixel_matrix, kernel_size)
    closed_image = apply_erosion(dilated_image, kernel_size)
    return closed_image

def apply_internal_border(pixel_matrix, kernel_size=3):
    """Calcula a borda interna de uma imagem (Original - Erodida)."""
    eroded_image = apply_erosion(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(pixel_matrix, eroded_image)

def apply_external_border(pixel_matrix, kernel_size=3):
    """Calcula a borda externa de uma imagem (Dilatada - Original)."""
    dilated_image = apply_dilation(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(dilated_image, pixel_matrix)

def apply_morphological_gradient(pixel_matrix, kernel_size=3):
    """Calcula o gradiente morfológico de uma imagem (Dilatação - Erosão)."""
    dilated_image = apply_dilation(pixel_matrix, kernel_size)
    eroded_image = apply_erosion(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(dilated_image, eroded_image)

def apply_top_hat(pixel_matrix, kernel_size=3):
    """Aplica a transformação Top-Hat (Original - Abertura)."""
    opened_image = apply_opening(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(pixel_matrix, opened_image)

def apply_bottom_hat(pixel_matrix, kernel_size=3):
    """Aplica a transformação Bottom-Hat (Fechamento - Original)."""
    closed_image = apply_closing(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(closed_image, pixel_matrix)

# --- Funções para Hit-or-Miss ---

def _apply_binary_erosion(binary_matrix, kernel):
    """Aplica erosão com um kernel específico em uma imagem binária (0 ou 1)."""
    height = len(binary_matrix)
    width = len(binary_matrix[0])
    kh, kw = len(kernel), len(kernel[0])
    offset_y, offset_x = kh // 2, kw // 2
    
    eroded_image = [[0 for _ in range(width)] for _ in range(height)]
    
    for y in range(offset_y, height - offset_y):
        for x in range(offset_x, width - offset_x):
            match = True
            for i in range(kh):
                for j in range(kw):
                    if kernel[i][j] == 1:
                        if binary_matrix[y + i - offset_y][x + j - offset_x] == 0:
                            match = False
                            break
                if not match:
                    break
            if match:
                eroded_image[y][x] = 1
                
    return eroded_image

def apply_hit_or_miss(binary_matrix, kernel_j, kernel_k):
    """
    Aplica o operador Hit-or-Miss.
    A imagem deve ser binária (0s e 1s).
    A = imagem original.
    A^c = complemento da imagem.
    Resultado = (A erodido por J) INTERSEÇÃO (A^c erodido por K)
    """
    # 1. Erosão da imagem original pelo kernel J (Hit)
    erosion_j = _apply_binary_erosion(binary_matrix, kernel_j)
    
    # 2. Criação do complemento da imagem
    complement_matrix = [[1 - pixel for pixel in row] for row in binary_matrix]
    
    # 3. Erosão do complemento pelo kernel K (Miss)
    erosion_k = _apply_binary_erosion(complement_matrix, kernel_k)
    
    # 4. Interseção (AND) dos dois resultados
    height = len(binary_matrix)
    width = len(binary_matrix[0])
    result = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if erosion_j[y][x] == 1 and erosion_k[y][x] == 1:
                result[y][x] = 1
                
    return result

