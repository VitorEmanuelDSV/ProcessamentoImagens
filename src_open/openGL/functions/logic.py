import numpy as np

def logico_or(img1, img2):
    altura, largura = img1.shape
    resultado = [[0]*largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            resultado[y][x] = int(img1[y][x]) | int(img2[y][x])
    return np.array(resultado, dtype=np.uint8)

def logico_and(img1, img2):
    altura, largura = img1.shape
    resultado = [[0]*largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            resultado[y][x] = int(img1[y][x]) & int(img2[y][x])
    return np.array(resultado, dtype=np.uint8)

def logico_xor(img1, img2):
    altura, largura = img1.shape
    resultado = [[0]*largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            resultado[y][x] = int(img1[y][x]) ^ int(img2[y][x])
    return np.array(resultado, dtype=np.uint8)