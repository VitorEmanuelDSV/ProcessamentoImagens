def or_imagens(img1, img2):
    """
    Aplica a operação lógica OR pixel a pixel entre duas imagens.
    """
    print(">>> LÓGICA: Operação OR...")
    if not img1 or not img2:
        return None

    height = min(len(img1), len(img2))
    width = min(len(img1[0]), len(img2[0]))
    resultado = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            resultado[y][x] = img1[y][x] | img2[y][x]

    return resultado

def and_imagens(img1, img2):
    """
    Aplica a operação lógica AND pixel a pixel entre duas imagens.
    """
    print(">>> LÓGICA: Operação AND...")
    if not img1 or not img2:
        return None

    height = min(len(img1), len(img2))
    width = min(len(img1[0]), len(img2[0]))
    resultado = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            resultado[y][x] = img1[y][x] & img2[y][x]

    return resultado

def xor_imagens(img1, img2):
    """
    Aplica a operação lógica XOR pixel a pixel entre duas imagens.
    """
    print(">>> LÓGICA: Operação XOR...")
    if not img1 or not img2:
        return None

    height = min(len(img1), len(img2))
    width = min(len(img1[0]), len(img2[0]))
    resultado = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            resultado[y][x] = img1[y][x] ^ img2[y][x]

    return resultado
