import numpy as np

class Linha:
    def __init__(self, p1, p2):
        self.P = np.array(p1, dtype=float)
        self.Q = np.array(p2, dtype=float)
        self.vetor_PQ = self.Q - self.P
        self.vetor_perpendicular = np.array([-self.vetor_PQ[1], self.vetor_PQ[0]])
        self.comprimento_quadrado = self.vetor_PQ[0]**2 + self.vetor_PQ[1]**2
        if self.comprimento_quadrado == 0:
            self.comprimento_quadrado = 1e-6

    def obter_coords_relativas(self, X):
        vetor_PX = X - self.P
        u = np.dot(vetor_PX, self.vetor_PQ) / self.comprimento_quadrado
        v = np.dot(vetor_PX, self.vetor_perpendicular) / np.sqrt(self.comprimento_quadrado)
        return u, v

    def obter_ponto_absoluto(self, u, v):
        return self.P + u * self.vetor_PQ + (v * self.vetor_perpendicular) / np.sqrt(self.comprimento_quadrado)

def deformar_imagem(img_origem, pontos_origem, pontos_destino, a=1.0, b=2.0, p=0.5):
    num_linhas = len(pontos_origem) // 2
    linhas_origem = [Linha(pontos_origem[i*2], pontos_origem[i*2+1]) for i in range(num_linhas)]
    linhas_destino = [Linha(pontos_destino[i*2], pontos_destino[i*2+1]) for i in range(num_linhas)]

    altura, largura = img_origem.shape
    img_deformada = np.zeros_like(img_origem)

    for y_dst in range(altura):
        for x_dst in range(largura):
            ponto_X = np.array([x_dst, y_dst])
            deslocamento_total = np.zeros(2, dtype=float)
            peso_total = 0.0

            for i in range(num_linhas):
                linha_dst = linhas_destino[i]
                linha_src = linhas_origem[i]

                u, v = linha_dst.obter_coords_relativas(ponto_X)
                ponto_X_fonte = linha_src.obter_ponto_absoluto(u, v)
                deslocamento = ponto_X_fonte - ponto_X

                if 0 <= u <= 1:
                    dist = abs(v)
                elif u < 0:
                    dist = np.linalg.norm(ponto_X - linha_dst.P)
                else:
                    dist = np.linalg.norm(ponto_X - linha_dst.Q)

                peso = (linha_src.comprimento_quadrado ** p / (a + dist)) ** b
                deslocamento_total += deslocamento * peso
                peso_total += peso

            if peso_total > 1e-6:
                ponto_final_fonte = ponto_X + deslocamento_total / peso_total
            else:
                ponto_final_fonte = ponto_X

            x_src, y_src = ponto_final_fonte
            if 0 <= x_src < largura - 1 and 0 <= y_src < altura - 1:
                x1, y1 = int(x_src), int(y_src)
                x2, y2 = x1 + 1, y1 + 1
                fx, fy = x_src - x1, y_src - y1

                c1 = img_origem[y1, x1] * (1 - fx) + img_origem[y1, x2] * fx
                c2 = img_origem[y2, x1] * (1 - fx) + img_origem[y2, x2] * fx
                cor = c1 * (1 - fy) + c2 * fy
                img_deformada[y_dst, x_dst] = np.clip(cor, 0, 255)

    return img_deformada.astype(np.uint8)

def morph(img_inicial, img_final, pontos_inicial, pontos_final, t):
    pontos_intermediarios = (1 - t) * pontos_inicial + t * pontos_final
    img_inicial_deformada = deformar_imagem(img_inicial, pontos_inicial, pontos_intermediarios)
    img_final_deformada = deformar_imagem(img_final, pontos_final, pontos_intermediarios)
    return ((1 - t) * img_inicial_deformada.astype(float) + t * img_final_deformada.astype(float)).astype(np.uint8)