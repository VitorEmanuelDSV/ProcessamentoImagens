# src/algorithms/histogram.py

from tkinter import Toplevel, Canvas, Label

def equalizacao_histograma(imagem):
    """
    Aplica equalização de histograma em uma imagem em tons de cinza.
    A imagem é uma matriz (lista de listas) com valores de 0 a 255.
    """
    print(">>> LÓGICA: Equalização de Histograma")
    if not imagem:
        return None

    altura = len(imagem)
    largura = len(imagem[0])
    total_pixels = altura * largura

    # 1. Calcular o histograma
    histograma = [0] * 256
    for y in range(altura):
        for x in range(largura):
            intensidade = imagem[y][x]
            histograma[intensidade] += 1

    # 2. Calcular a CDF (função de distribuição acumulada)
    cdf = [0] * 256
    acumulado = 0
    for i in range(256):
        acumulado += histograma[i]
        cdf[i] = acumulado

    # 3. Normalizar a CDF
    cdf_min = next((valor for valor in cdf if valor > 0), 0)
    
    # Denominador para a normalização
    denominador = total_pixels - cdf_min
    if denominador == 0:
        # Se todos os pixels tiverem a mesma cor, retorna a imagem original
        return imagem

    cdf_normalizado = [0] * 256
    for i in range(256):
        cdf_normalizado[i] = round(((cdf[i] - cdf_min) / denominador) * 255)
        cdf_normalizado[i] = max(0, min(255, cdf_normalizado[i]))

    # 4. Criar imagem resultante com valores equalizados
    resultado = [[0 for _ in range(largura)] for _ in range(altura)]
    for y in range(altura):
        for x in range(largura):
            intensidade = imagem[y][x]
            resultado[y][x] = cdf_normalizado[intensidade]

    return resultado

def gerar_histograma(imagem):
    """
    Gera o histograma (contagem de intensidade 0–255) da imagem.
    """
    histograma = [0] * 256
    for linha in imagem:
        for intensidade in linha:
            histograma[intensidade] += 1
    return histograma

def desenhar_histograma(canvas, histograma, max_freq, altura_canvas, largura_canvas):
    """
    Desenha manualmente as barras de um histograma em um Canvas.
    """
    largura_barra = largura_canvas / 256.0
    for x in range(256):
        freq = histograma[x]
        altura_barra = int((freq / max_freq) * (altura_canvas - 10)) if max_freq > 0 else 0
        x0 = x * largura_barra
        y0 = altura_canvas
        x1 = (x + 1) * largura_barra
        y1 = altura_canvas - altura_barra
        canvas.create_rectangle(x0, y0, x1, y1, fill="black", outline="")

def mostrar_histogramas(parent, imagem_original, imagem_equalizada):
    """
    Mostra uma janela com os histogramas desenhados manualmente.
    """
    hist_original = gerar_histograma(imagem_original)
    hist_equalizado = gerar_histograma(imagem_equalizada)

    # Encontra a frequência máxima entre os dois histogramas para uma escala consistente
    try:
        max_freq = max(max(hist_original), max(hist_equalizado))
    except ValueError:
        max_freq = 1 # Evita erro se o histograma estiver vazio

    altura_canvas = 256
    largura_canvas = 512

    janela = Toplevel(parent)
    janela.title("Histogramas")
    janela.configure(bg="#2e2e2e")
    
    # Estilo dos labels
    label_style = {'bg': "#2e2e2e", 'fg': "#dcdcdc", 'font': ('Arial', 12)}

    Label(janela, text="Histograma Original", **label_style).pack(pady=(10,2))
    canvas_original = Canvas(janela, width=largura_canvas, height=altura_canvas, bg="white")
    canvas_original.pack(padx=10, pady=(0, 10))
    desenhar_histograma(canvas_original, hist_original, max_freq, altura_canvas, largura_canvas)

    Label(janela, text="Histograma Equalizado", **label_style).pack(pady=(10,2))
    canvas_equalizado = Canvas(janela, width=largura_canvas, height=altura_canvas, bg="white")
    canvas_equalizado.pack(padx=10, pady=(0, 10))
    desenhar_histograma(canvas_equalizado, hist_equalizado, max_freq, altura_canvas, largura_canvas)
