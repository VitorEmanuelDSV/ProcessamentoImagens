import numpy as np

def morfismo_tempo(img1, img2, t):
    if img1.shape != img2.shape:
        raise ValueError("As imagens devem ter as mesmas dimensões")

    resultado = (1 - t) * img1 + t * img2
    resultado = np.clip(resultado, 0, 255).astype(np.uint8)
    return resultado
