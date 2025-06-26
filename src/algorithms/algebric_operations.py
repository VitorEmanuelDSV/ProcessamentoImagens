# src/algorithms/algebric_operations.py

def somar_imagens(img1, img2):
    """
    Soma pixel a pixel entre duas imagens, ajustando para o menor tamanho comum.
    """
    print(">>> LÓGICA: Somando imagens...")

    if not img1 or not img2:
        return None

    height = min(len(img1), len(img2))
    width = min(len(img1[0]), len(img2[0]))

    resultado = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            soma = img1[y][x] + img2[y][x]
            resultado[y][x] = min(soma, 255)

    return resultado

def subtrair_imagens(img1, img2):
    """
    Realiza a subtração pixel a pixel de duas imagens, ajustando para o menor tamanho.
    """
    print(">>> LÓGICA: Subtraindo imagens...")
    if not img1 or not img2:
        return None

    height = min(len(img1), len(img2))
    width = min(len(img1[0]), len(img2[0]))
    resultado = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            subtracao = img1[y][x] - img2[y][x]
            resultado[y][x] = max(subtracao, 0) 

    return resultado

def multiplicar_imagem(img1, fator):
    """
    Multiplica os pixels da imagem por um fator escalar.
    """
    print(">>> LÓGICA: Multiplicando imagem por fator...")
    if not img1:
        return None

    height = len(img1)
    width = len(img1[0])
    resultado = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            produto = img1[y][x] * fator
            resultado[y][x] = min(int(round(produto)), 255)

    return resultado

def dividir_imagem(img1, fator):
    """
    Divide os pixels da imagem por um fator escalar.
    """
    print(">>> LÓGICA: Dividindo imagem por fator...")
    if not img1 or fator == 0:
        return None

    height = len(img1)
    width = len(img1[0])
    resultado = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            divisao = img1[y][x] / fator
            resultado[y][x] = max(0, min(int(round(divisao)), 255))

    return resultado
