# src/algorithms/matrix_utils.py

def add_matrices(matrix1, matrix2):
    """
    Soma duas matrizes elemento a elemento.
    É uma aproximação da magnitude do gradiente |G| ≈ |Gx| + |Gy|.

    Args:
        matrix1 (list[list[int]]): A primeira matriz (ex: resultado de Gx).
        matrix2 (list[list[int]]): A segunda matriz (ex: resultado de Gy).

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
            # Soma os valores absolutos dos pixels de cada matriz
            sum_val = abs(matrix1[y][x]) + abs(matrix2[y][x])
            
            # Garante que o valor final esteja no intervalo [0, 255]
            if sum_val > 255:
                result_matrix[y][x] = 255
            else:
                result_matrix[y][x] = int(sum_val)
                
    return result_matrix
