from tkinter import Toplevel, Canvas, Label

def equalizacao_histograma(imagem):
    """
    Aplica equalização de histograma em uma imagem em tons de cinza.
    A imagem é uma matriz (lista de listas) com valores de 0 a 255.
    """
    print(">>> LÓGICA: Equalização de Histograma")

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
    cdf_normalizado = [0] * 256
    for i in range(256):
        if total_pixels - cdf_min == 0:
            cdf_normalizado[i] = 0
        else:
            cdf_normalizado[i] = round((cdf[i] - cdf_min) / (total_pixels - cdf_min) * 255)
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

def mostrar_histogramas(parent, imagem_original, imagem_equalizada):
    """
    Mostra uma janela com os histogramas desenhados manualmente.
    """
    hist_original = gerar_histograma(imagem_original)
    hist_equalizado = gerar_histograma(imagem_equalizada)

    max_freq = max(max(hist_original), max(hist_equalizado))
    altura_canvas = 300
    largura_canvas = 400

    janela = Toplevel(parent)
    janela.title("Histogramas")
    janela.geometry(f"{largura_canvas + 40}x{altura_canvas * 2 + 150}")
    janela.resizable(False, False)

    Label(janela, text="Histograma Original").pack()
    canvas_original = Canvas(janela, width=largura_canvas, height=altura_canvas, bg="white")
    canvas_original.pack(padx=10, pady=(0, 10))
    desenhar_histograma(canvas_original, hist_original, max_freq, altura_canvas)

    Label(janela, text="Histograma Equalizado").pack()
    canvas_equalizado = Canvas(janela, width=largura_canvas, height=altura_canvas, bg="white")
    canvas_equalizado.pack(padx=10, pady=(0, 10))
    desenhar_histograma(canvas_equalizado, hist_equalizado, max_freq, altura_canvas)

def desenhar_histograma(canvas, histograma, max_freq, altura_canvas):
    """
    Desenha manualmente as barras de um histograma em um Canvas.
    """
    for x in range(256):
        freq = histograma[x]
        altura = int((freq / max_freq) * (altura_canvas - 10)) if max_freq > 0 else 0
        canvas.create_line(x, altura_canvas, x, altura_canvas - altura, fill="black")