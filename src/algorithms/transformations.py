# src/algorithms/transformations.py

def aplicar_negativo(dados_imagem):
    """
    Esta função receberá os dados de uma imagem (ex: uma lista de listas de pixels)
    e deverá retornar os novos dados da imagem com o filtro negativo aplicado.
    
    A lógica S=255-r será implementada aqui.
    """
    print(">>> LÓGICA: Aplicando filtro negativo...")
    # Exemplo de lógica (será substituída pelos seus cálculos reais):
    # novos_dados = []
    # for linha in dados_imagem:
    #     nova_linha = []
    #     for pixel in linha:
    #         novo_pixel = 255 - pixel
    #         nova_linha.append(novo_pixel)
    #     novos_dados.append(nova_linha)
    # return novos_dados
    
    # Por enquanto, apenas imprimimos uma mensagem.
    return None

def aplicar_gamma(dados_imagem, gamma):
    """
    Aplica a transformação gamma. A lógica S = c*r^gamma será implementada aqui.
    """
    print(f">>> LÓGICA: Aplicando Gamma com valor {gamma}...")
    return None