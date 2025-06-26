# src/algorithms/filters.py

def apply_convolution(pixel_matrix, kernel):
    """
    Aplica uma operação de convolução 3x3 em uma matriz de pixels.
    Esta é a operação base para a maioria dos filtros espaciais.

    Args:
        pixel_matrix (list[list[int]]): A matriz 2D da imagem.
        kernel (list[list[float]]): A matriz do kernel 3x3.

    Returns:
        list[list[int]]: A nova matriz de pixels após a convolução.
    """
    if not pixel_matrix or not kernel:
        return None

    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            
            weighted_sum = 0.0
            for i in range(3):
                for j in range(3):
                    pixel_value = pixel_matrix[y + i - 1][x + j - 1]
                    kernel_value = kernel[i][j]
                    weighted_sum += pixel_value * kernel_value
            
            if weighted_sum < 0:
                output_matrix[y][x] = 0
            elif weighted_sum > 255:
                output_matrix[y][x] = 255
            else:
                output_matrix[y][x] = int(round(weighted_sum))
    
    return output_matrix

def apply_mean_filter(pixel_matrix):
    """
    Define o kernel do filtro da média e chama a função de convolução.
    """
    mean_kernel = [
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9]
    ]
    return apply_convolution(pixel_matrix, mean_kernel)

def apply_median_filter(pixel_matrix):
    """
    Aplica o filtro da mediana em uma imagem.
    """
    if not pixel_matrix:
        return None

    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            
            neighbors = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    neighbors.append(pixel_matrix[y + i][x + j])
            
            neighbors.sort()
            median_value = neighbors[4]
            output_matrix[y][x] = median_value
            
    return output_matrix

def apply_edge_detection_filter(pixel_matrix):
    """
    Aplica um filtro Laplaciano para detecção de bordas.
    """
    edge_kernel = [
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ]
    return apply_convolution(pixel_matrix, edge_kernel)

def apply_high_pass_basic_filter(pixel_matrix):
    """
    Aplica um filtro passa-alta básico (high-boost).
    """
    high_pass_kernel = [
        [-1, -1, -1],
        [-1,  9, -1],
        [-1, -1, -1]
    ]
    return apply_convolution(pixel_matrix, high_pass_kernel)
