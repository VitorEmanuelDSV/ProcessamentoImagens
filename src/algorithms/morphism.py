def aplicar_morfismo(img1, img2, t):
    """
    Aplica a interpolação linear (morfismo) entre duas imagens:
    resultado = (1 - t) * img1 + t * img2

    Onde t ∈ [0, 1]
    """
    print(f">>> LÓGICA: Morfismo com t = {t}")

    if not img1 or not img2:
        return None

    altura = min(len(img1), len(img2))
    largura = min(len(img1[0]), len(img2[0]))
    resultado = [[0 for _ in range(largura)] for _ in range(altura)]

    for y in range(altura):
        for x in range(largura):
            valor = (1 - t) * img1[y][x] + t * img2[y][x]
            resultado[y][x] = max(0, min(int(round(valor)), 255))

    return resultado
