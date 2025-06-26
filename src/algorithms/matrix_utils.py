# src/algorithms/matrix_utils.py

def add_matrices_simple(matrix1, matrix2):
    """Soma duas matrizes elemento a elemento com clamping."""
    if not matrix1 or not matrix2 or len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        return None
    height = len(matrix1)
    width = len(matrix1[0])
    result_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            sum_val = matrix1[y][x] + matrix2[y][x]
            if sum_val > 255: result_matrix[y][x] = 255
            elif sum_val < 0: result_matrix[y][x] = 0
            else: result_matrix[y][x] = int(sum_val)
    return result_matrix

def add_gradient_matrices(matrix1, matrix2):
    """Soma os valores absolutos de duas matrizes (para gradientes)."""
    if not matrix1 or not matrix2 or len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        return None
    height = len(matrix1)
    width = len(matrix1[0])
    result_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            sum_val = abs(matrix1[y][x]) + abs(matrix2[y][x])
            if sum_val > 255: result_matrix[y][x] = 255
            else: result_matrix[y][x] = int(sum_val)
    return result_matrix

def subtract_matrices(matrix1, matrix2):
    """Subtrai a segunda matriz da primeira, elemento a elemento."""
    if not matrix1 or not matrix2 or len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        return None
    height = len(matrix1)
    width = len(matrix1[0])
    result_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            sub_val = matrix1[y][x] - matrix2[y][x]
            if sub_val < 0: result_matrix[y][x] = 0
            else: result_matrix[y][x] = int(sub_val)
    return result_matrix

def multiply_by_scalar(matrix, scalar):
    """Multiplica cada elemento de uma matriz por um valor escalar."""
    if not matrix:
        return None
    height = len(matrix)
    width = len(matrix[0])
    result_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            result_matrix[y][x] = matrix[y][x] * scalar
    return result_matrix
