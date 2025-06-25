import numpy as np

def soma(img1, img2):
    altura, largura = img1.shape
    resultado = [[0]*largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            soma = int(img1[y][x]) + int(img2[y][x])
            resultado[y][x] = min(255, soma)
    return np.array(resultado, dtype=np.uint8)

def subtracao(img1, img2):
    altura, largura = img1.shape
    resultado = [[0]*largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            sub = int(img1[y][x]) - int(img2[y][x])
            resultado[y][x] = max(0, sub)
    return np.array(resultado, dtype=np.uint8)

def multiplicacao(img1, img2):
    altura, largura = img1.shape
    resultado = [[0]*largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            mult = (int(img1[y][x]) * int(img2[y][x])) // 255
            resultado[y][x] = min(255, mult)
    return np.array(resultado, dtype=np.uint8)

def divisao(img1, img2):
    altura, largura = img1.shape
    resultado = [[0]*largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            a = int(img1[y][x])
            b = int(img2[y][x])
            if b == 0:
                resultado[y][x] = 0
            else:
                div = int((a / b) * 255)
                resultado[y][x] = min(255, div)
    return np.array(resultado, dtype=np.uint8)