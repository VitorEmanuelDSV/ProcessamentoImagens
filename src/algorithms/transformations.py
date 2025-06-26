# src/algorithms/transformations.py

def apply_negative(pixel_matrix):
    """
    Calcula o negativo de uma imagem.
    Aplica a fórmula S = 255 - r para cada pixel.

    Args:
        pixel_matrix (list[list[int]]): A matriz 2D da imagem.

    Returns:
        list[list[int]]: A nova matriz de pixels com a transformação negativa.
    """
    if not pixel_matrix:
        return None

    height = len(pixel_matrix)
    width = len(pixel_matrix[0])
    
    # Cria uma nova matriz para armazenar o resultado
    output_matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            original_pixel = pixel_matrix[y][x]
            # Aplica a fórmula do negativo
            output_matrix[y][x] = 255 - original_pixel
            
    return output_matrix
