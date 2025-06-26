# src/algorithms/filters.py

from src.algorithms import matrix_utils

def apply_convolution(pixel_matrix, kernel):
    """Aplica uma operação de convolução 3x3 em uma matriz de pixels."""
    if not pixel_matrix or not kernel: return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            weighted_sum = sum(
                pixel_matrix[y + i - 1][x + j - 1] * kernel[i][j]
                for i in range(3) for j in range(3)
            )
            output_matrix[y][x] = int(round(weighted_sum))
    return output_matrix

def apply_clamping(pixel_matrix):
    """Garante que todos os pixels estejam no intervalo [0, 255]."""
    if not pixel_matrix: return None
    return [[max(0, min(255, pixel)) for pixel in row] for row in pixel_matrix]

def apply_mean_filter(pixel_matrix):
    mean_kernel = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]
    return apply_clamping(apply_convolution(pixel_matrix, mean_kernel))

def apply_median_filter(pixel_matrix):
    if not pixel_matrix: return None
    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            neighbors = sorted([pixel_matrix[y+i][x+j] for i in range(-1, 2) for j in range(-1, 2)])
            output_matrix[y][x] = neighbors[4]
    return output_matrix

def apply_edge_detection_filter(pixel_matrix):
    edge_kernel = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    return apply_clamping(apply_convolution(pixel_matrix, edge_kernel))

def apply_high_pass_basic_filter(pixel_matrix):
    high_pass_kernel = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
    return apply_clamping(apply_convolution(pixel_matrix, high_pass_kernel))

def apply_roberts_filter(pixel_matrix):
    kernel_x = [[0,0,0],[0,1,0],[0,-1,0]]
    kernel_y = [[0,0,0],[0,1,-1],[0,0,0]]
    gx_matrix = apply_convolution(pixel_matrix, kernel_x)
    gy_matrix = apply_convolution(pixel_matrix, kernel_y)
    return matrix_utils.add_gradient_matrices(gx_matrix, gy_matrix)

def apply_roberts_cross_filter(pixel_matrix):
    kernel_x = [[0,0,0],[0,1,0],[0,0,-1]]
    kernel_y = [[0,0,0],[0,0,1],[0,-1,0]]
    gx_matrix = apply_convolution(pixel_matrix, kernel_x)
    gy_matrix = apply_convolution(pixel_matrix, kernel_y)
    return matrix_utils.add_gradient_matrices(gx_matrix, gy_matrix)

def apply_prewitt_filter(pixel_matrix):
    kernel_gx = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    kernel_gy = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
    gx_matrix = apply_convolution(pixel_matrix, kernel_gx)
    gy_matrix = apply_convolution(pixel_matrix, kernel_gy)
    return matrix_utils.add_gradient_matrices(gx_matrix, gy_matrix)

def apply_sobel_filter(pixel_matrix):
    kernel_gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    kernel_gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    gx_matrix = apply_convolution(pixel_matrix, kernel_gx)
    gy_matrix = apply_convolution(pixel_matrix, kernel_gy)
    return matrix_utils.add_gradient_matrices(gx_matrix, gy_matrix)

def apply_high_boost_filter(pixel_matrix, factor_a):
    high_pass_kernel = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    high_pass_image = apply_convolution(pixel_matrix, high_pass_kernel)
    scaled_high_pass = matrix_utils.multiply_by_scalar(high_pass_image, factor_a)
    boosted_image = matrix_utils.add_matrices_simple(pixel_matrix, scaled_high_pass)
    return boosted_image
