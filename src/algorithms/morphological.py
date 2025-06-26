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

def apply_opening(pixel_matrix, kernel_size=3):
    """
    Aplica a operação de abertura morfológica (Erosão -> Dilatação).
    """
    eroded_image = apply_erosion(pixel_matrix, kernel_size)
    opened_image = apply_dilation(eroded_image, kernel_size)
    return opened_image

def apply_closing(pixel_matrix, kernel_size=3):
    """
    Aplica a operação de fechamento morfológico (Dilatação -> Erosão).
    """
    dilated_image = apply_dilation(pixel_matrix, kernel_size)
    closed_image = apply_erosion(dilated_image, kernel_size)
    return closed_image

def apply_internal_border(pixel_matrix, kernel_size=3):
    """
    Calcula a borda interna de uma imagem (Original - Erodida).
    """
    eroded_image = apply_erosion(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(pixel_matrix, eroded_image)

def apply_external_border(pixel_matrix, kernel_size=3):
    """
    Calcula a borda externa de uma imagem (Dilatada - Original).
    """
    dilated_image = apply_dilation(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(dilated_image, pixel_matrix)

def apply_morphological_gradient(pixel_matrix, kernel_size=3):
    """
    Calcula o gradiente morfológico de uma imagem (Dilatação - Erosão).
    """
    dilated_image = apply_dilation(pixel_matrix, kernel_size)
    eroded_image = apply_erosion(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(dilated_image, eroded_image)

def apply_top_hat(pixel_matrix, kernel_size=3):
    """
    Aplica a transformação Top-Hat (Original - Abertura).
    Realça pequenos detalhes claros em fundos escuros.
    """
    opened_image = apply_opening(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(pixel_matrix, opened_image)

def apply_bottom_hat(pixel_matrix, kernel_size=3):
    """
    Aplica a transformação Bottom-Hat (Fechamento - Original).
    Realça pequenos detalhes escuros em fundos claros.
    """
    closed_image = apply_closing(pixel_matrix, kernel_size)
    return matrix_utils.subtract_matrices(closed_image, pixel_matrix)
