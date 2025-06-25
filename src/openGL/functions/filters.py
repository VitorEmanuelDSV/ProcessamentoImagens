import numpy as np

def filtro_media(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros_like(imagem)

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            vizinhos = imagem[y-1:y+2, x-1:x+2]
            media = int(np.mean(vizinhos))
            resultado[y, x] = media

    return resultado

def filtro_mediana(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros_like(imagem)

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            vizinhos = imagem[y-1:y+2, x-1:x+2].flatten()
            mediana = int(np.median(vizinhos))
            resultado[y, x] = mediana

    return resultado

def filtro_passa_alta(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros_like(imagem)

    kernel = np.array([[ -1, -1, -1],
                       [ -1,  8, -1],
                       [ -1, -1, -1]])

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            região = imagem[y-1:y+2, x-1:x+2]
            valor = np.sum(kernel * região)
            resultado[y, x] = np.clip(valor, 0, 255)

    return resultado

def filtro_sobel(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros_like(imagem)

    gx_kernel = np.array([[-1, 0, 1],
                          [-2, 0, 2],
                          [-1, 0, 1]])
    gy_kernel = np.array([[ 1,  2,  1],
                          [ 0,  0,  0],
                          [-1, -2, -1]])

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            região = imagem[y-1:y+2, x-1:x+2]
            gx = np.sum(gx_kernel * região)
            gy = np.sum(gy_kernel * região)
            magnitude = np.clip(abs(gx) + abs(gy), 0, 255)
            resultado[y, x] = magnitude

    return resultado

def filtro_roberts(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros_like(imagem)

    for y in range(altura - 1):
        for x in range(largura - 1):
            gx = int(imagem[y, x]) - int(imagem[y+1, x+1])
            gy = int(imagem[y+1, x]) - int(imagem[y, x+1])
            magnitude = np.clip(abs(gx) + abs(gy), 0, 255)
            resultado[y, x] = magnitude

    return resultado

def filtro_prewitt(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros_like(imagem)

    gx_kernel = np.array([[-1, 0, 1],
                          [-1, 0, 1],
                          [-1, 0, 1]])
    gy_kernel = np.array([[ 1,  1,  1],
                          [ 0,  0,  0],
                          [-1, -1, -1]])

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            região = imagem[y-1:y+2, x-1:x+2]
            gx = np.sum(gx_kernel * região)
            gy = np.sum(gy_kernel * região)
            magnitude = np.clip(abs(gx) + abs(gy), 0, 255)
            resultado[y, x] = magnitude

    return resultado

def filtro_high_boost(imagem, A=1.5):
    altura, largura = imagem.shape
    resultado = np.zeros_like(imagem)

    # Passa-baixa com média
    blur = filtro_media(imagem)
    mascara = imagem - blur
    resultado = imagem + A * mascara
    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    return resultado

def equalizacao_histograma(imagem):
    altura, largura = imagem.shape
    total_pixels = altura * largura

    histograma = [0] * 256
    for y in range(altura):
        for x in range(largura):
            intensidade = imagem[y, x]
            histograma[intensidade] += 1

    cdf = [0] * 256
    acumulado = 0
    for i in range(256):
        acumulado += histograma[i]
        cdf[i] = acumulado

    cdf_min = next(valor for valor in cdf if valor > 0)
    cdf_normalizado = [0] * 256
    for i in range(256):
        cdf_normalizado[i] = round((cdf[i] - cdf_min) / (total_pixels - cdf_min) * 255)
        cdf_normalizado[i] = max(0, min(255, cdf_normalizado[i]))

    resultado = [[0] * largura for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            intensidade = imagem[y, x]
            resultado[y][x] = cdf_normalizado[intensidade]

    return np.array(resultado, dtype=np.uint8)