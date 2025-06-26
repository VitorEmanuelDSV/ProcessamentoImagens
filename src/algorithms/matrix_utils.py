# src/algorithms/matrix_utils.py

def add_matrices(matrix1, matrix2):
    """
    Soma duas matrizes elemento a elemento.

    Args:
        matrix1 (list[list[int]]): A primeira matriz.
        matrix2 (list[list[int]]): A segunda matriz.

    Returns:
        list[list[int]]: A matriz resultante da soma.
    """
    if not matrix1 or not matrix2 or len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        print("Erro: As matrizes devem existir e ter as mesmas dimensões.")
        return None

    height = len(matrix1)
    width = len(matrix1[0])
    
    result_matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            # Soma os valores dos pixels de cada matriz
            # Na detecção de bordas, os valores absolutos são usados. Para high-boost, a soma direta.
            # Aqui, implementamos a soma direta, que é mais geral.
            sum_val = matrix1[y][x] + matrix2[y][x]
            
            # Garante que o valor final esteja no intervalo [0, 255]
            if sum_val > 255:
                result_matrix[y][x] = 255
            elif sum_val < 0:
                result_matrix[y][x] = 0
            else:
                result_matrix[y][x] = int(sum_val)
                
    return result_matrix

def multiply_by_scalar(matrix, scalar):
    """
    Multiplica cada elemento de uma matriz por um valor escalar.

    Args:
        matrix (list[list[int]]): A matriz a ser multiplicada.
        scalar (float): O fator de multiplicação.

    Returns:
        list[list[int]]: A matriz resultante.
    """
    if not matrix:
        return None

    height = len(matrix)
    width = len(matrix[0])
    
    result_matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            result_matrix[y][x] = matrix[y][x] * scalar
            
    return result_matrix
