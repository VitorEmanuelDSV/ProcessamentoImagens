import os
import threading
from openGL.functions.primitives import draw_pixel, load_pgm_ascii
from openGL.functions.filters import (
    filtro_media, filtro_mediana, filtro_passa_alta,
    filtro_roberts, filtro_sobel, filtro_prewitt,
    filtro_high_boost, equalizacao_histograma
)
from openGL.functions.algebraic import soma, subtracao, multiplicacao, divisao
from openGL.functions.logic import logico_and, logico_or, logico_xor
from openGL.functions.morphology import morfismo_tempo

class OpenGLManager:
    def __init__(self, app_ref=None):
        self.running = True
        self.image = None
        self.filtered_image = None
        self.image2 = None
        self.app_ref = app_ref

    def menu(self):
        while self.running:
            print("\n=== Menu Principal ===")
            print("0 - Carregar Imagem")
            print("1 - Filtros")
            print("2 - Operações Algébricas")
            print("3 - Operações Lógicas")
            print("q - Sair")

            escolha = input("Digite a opção desejada: ").strip()

            if escolha == '0':
                img = input("Carregar imagem (1) ou (2): ").strip()
                self.menu_load_image('image' if img == '1' else 'image2')
            elif escolha == '1':
                self.menu_filtros()
            elif escolha == '2':
                self.menu_algebrico()
            elif escolha == '3':
                self.menu_logico()
            elif escolha.lower() == 'q':
                self.running = False
                os._exit(0)
            else:
                print("Opção inválida. Tente novamente.")

    def menu_filtros(self):
        while self.running:
            print("\n=== Menu Principal ===")
            print("1 - Filtro da Média")
            print("2 - Filtro da Mediana")
            print("3 - Filtro Passa-Alta")
            print("4 - Filtro Roberts")
            print("5 - Filtro Sobel")
            print("6 - Filtro Prewitt")
            print("7 - Filtro High-Boost")
            print("8 - Equalização de Histograma")
            print("q - Voltar")

            escolha = input("Digite a opção desejada: ").strip()

            if escolha == '1':
                self.apply_filtro_media()
            elif escolha == '2':
                self.apply_filtro_mediana()
            elif escolha == '3':
                self.apply_filtro_passa_alta()
            elif escolha == '4':
                self.apply_filtro_roberts()
            elif escolha == '5':
                self.apply_filtro_sobel()
            elif escolha == '6':
                self.apply_filtro_prewitt()
            elif escolha == '7':
                self.apply_filtro_high_boost()
            elif escolha == '8':
                self.apply_equalizacao_histograma()
            elif escolha.lower() == 'q':
                self.menu()
            else:
                print("Opção inválida. Tente novamente.")

    def menu_algebrico(self):
        while True:
            print("\n--- Operações Algébricas ---")
            print("1 - Soma")
            print("2 - Subtração")
            print("3 - Multiplicação")
            print("4 - Divisão")
            print("q - Voltar")

            escolha = input("Escolha a operação: ").strip()

            if escolha == '1':
                self.apply_soma()
            elif escolha == '2':
                self.apply_subtracao()
            elif escolha == '3':
                self.apply_multiplicacao()
            elif escolha == '4':
                self.apply_divisao()
            elif escolha.lower() == 'q':
                self.menu()
            else:
                print("Opção inválida.")

    def menu_logico(self):
        while True:
            print("\n--- Operações Lógicas ---")
            print("1 - OR")
            print("2 - AND")
            print("3 - XOR")
            print("4 - Morfismo Dependente do Tempo")
            print("q - Voltar")

            escolha = input("Escolha a operação lógica: ").strip()

            if escolha == '1':
                self.apply_logico_or()
            elif escolha == '2':
                self.apply_logico_and()
            elif escolha == '3':
                self.apply_logico_xor()
            elif escolha == '4':
                self.apply_morfismo_tempo()
            elif escolha.lower() == 'q':
                break
            else:
                print("Opção inválida.")

    def menu_load_image(self, destino='image'):
        print(f"\n--- Carregar Imagem para {destino} ---\n")
        print("1 - Airplane.pgm")
        print("2 - Iena.pgm")
        print("3 - Lenag.pgm")
        print("4 - Lenasalp.pgm")
        print("5 - me_child.pgm")
        print("6 - me_now.pgm")

        opcao = input("Selecione a imagem (1 a 4): ").strip()

        img = ""
        if opcao == "1":
            img = "Airplane.pgm"
        elif opcao == "2":
            img = "Lena.pgm"
        elif opcao == "3":
            img = "Lenag.pgm"
        elif opcao == "4":
            img = "Lenasalp.pgm"
        elif opcao == "5":
            img = "me_child.pgm"
        elif opcao == "6":
            img = "me_now.pgm"
        else:
            print("Opção inválida.")
            return

        caminho = os.path.join("src", "assets", img)
        print(f"[DEBUG] Tentando carregar: {caminho}")
        if os.path.isfile(caminho):
            self.load_image(caminho, destino)
            if self.app_ref:
                self.app_ref.after(0, self.app_ref.redraw)
            print(f"Imagem '{img}' carregada em '{destino}' com sucesso.")
        else:
            print("Arquivo não encontrado.")

    #region Filters
    def apply_filtro_media(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando filtro da média...")
        self.filtered_image = filtro_media(self.image)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_filtro_mediana(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando filtro da mediana...")
        self.filtered_image = filtro_mediana(self.image)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_filtro_passa_alta(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando filtro passa-alta...")
        self.filtered_image = filtro_passa_alta(self.image)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_filtro_roberts(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando filtro de Roberts...")
        self.filtered_image = filtro_roberts(self.image)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_filtro_sobel(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando filtro de Sobel...")
        self.filtered_image = filtro_sobel(self.image)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_filtro_prewitt(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando filtro de Prewitt...")
        self.filtered_image = filtro_prewitt(self.image)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_filtro_high_boost(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando filtro High-Boost...")
        self.filtered_image = filtro_high_boost(self.image, A=1.5)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_equalizacao_histograma(self):
        if self.image is None:
            print("Nenhuma imagem carregada.")
            return

        print("Aplicando equalização de histograma...")
        self.filtered_image = equalizacao_histograma(self.image)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)
    #endregion

    #region Algebraic
    def apply_soma(self):
            if self.image is None or self.image2 is None:
                print("Imagens não carregadas.")
                return
            print("Aplicando soma...")
            self.filtered_image = soma(self.image, self.image2)
            if self.app_ref:
                self.app_ref.after(0, self.app_ref.redraw)

    def apply_subtracao(self):
        if self.image is None or self.image2 is None:
            print("Imagens não carregadas.")
            return
        print("Aplicando subtração...")
        self.filtered_image = subtracao(self.image, self.image2)
        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_multiplicacao(self):
        if self.image is None or self.image2 is None:
            print("Imagens não carregadas.")
            return
        print("Aplicando multiplicação...")
        self.filtered_image = multiplicacao(self.image, self.image2)
        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_divisao(self):
        if self.image is None or self.image2 is None:
            print("Imagens não carregadas.")
            return
        print("Aplicando divisão...")
        self.filtered_image = divisao(self.image, self.image2)
        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)
    #endregion

    #region Logic
    def apply_logico_or(self):
        if self.image is None or self.image2 is None:
            print("Imagens não carregadas.")
            return
        print("Aplicando operação lógica OR...")
        self.filtered_image = logico_or(self.image, self.image2)
        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_logico_and(self):
        if self.image is None or self.image2 is None:
            print("Imagens não carregadas.")
            return
        print("Aplicando operação lógica AND...")
        self.filtered_image = logico_and(self.image, self.image2)
        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)

    def apply_logico_xor(self):
        if self.image is None or self.image2 is None:
            print("Imagens não carregadas.")
            return
        print("Aplicando operação lógica XOR...")
        self.filtered_image = logico_xor(self.image, self.image2)
        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)
    #endregion

    #region Morphology
    def apply_morfismo_tempo(self):
        if self.image is None or self.image2 is None:
            print("Imagens não carregadas.")
            return

        try:
            t = float(input("Digite o valor de t (0.0 a 1.0): ").strip())
            if not (0 <= t <= 1):
                raise ValueError
        except ValueError:
            print("Valor inválido para t.")
            return

        self.filtered_image = morfismo_tempo(self.image, self.image2, t)

        if self.app_ref:
            self.app_ref.after(0, self.app_ref.redraw)
    #endRegion

    # region Utils
    def start_menu_thread(self):
        menu_thread = threading.Thread(target=self.menu)
        menu_thread.daemon = True
        menu_thread.start()

    def load_image(self, path, destino='image'):
        imagem = load_pgm_ascii(path)
        if destino == 'image':
            self.image = imagem
            self.filtered_image = None
        elif destino == 'image2':
            self.image2 = imagem
        else:
            print("Destino inválido para carregar imagem.")

    def draw(self):
        if self.image is not None:
            altura, largura = self.image.shape

            # Imagem 1 - lado esquerdo
            for y in range(altura):
                for x in range(largura):
                    val = self.image[y, x] / 255.0
                    draw_pixel(x - largura - 20, altura // 2 - y, (val, val, val))

        if self.image2 is not None:
            altura, largura = self.image2.shape

            # Imagem 2 - centro
            for y in range(altura):
                for x in range(largura):
                    val = self.image2[y, x] / 255.0
                    draw_pixel(x + 10, altura // 2 - y, (val, val, val))

        if self.filtered_image is not None:
            altura, largura = self.filtered_image.shape

            # Resultado - lado direito
            for y in range(altura):
                for x in range(largura):
                    val = self.filtered_image[y, x] / 255.0
                    draw_pixel(x + largura + 40, altura // 2 - y, (val, val, val))
    #endregion