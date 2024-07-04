import pygame
from constantes import largura_tela, altura_tela, tamanho_sala 

def desenhar_cenario(tela, tamanho_sala):
    tela.fill(preto)
    for x in range(0, largura_tela, tamanho_sala):
        for y in range(0, altura_tela, tamanho_sala):
            pygame.draw.rect(tela, branco, (x, y, tamanho_sala, tamanho_sala))
            pygame.draw.rect(tela, preto, (x, y, tamanho_sala, tamanho_sala), 2)

    # Desenho dos elementos alinhados (sem centralização quando há mais de um)
    for x in range(0, largura_tela, tamanho_sala):
        for y in range(0, altura_tela, tamanho_sala):
            elementos_na_posicao = []
            for elemento, posicoes in posicoes_elementos.items():
                if isinstance(posicoes, list):
                    if (x, y) in posicoes:
                        elementos_na_posicao.append(elemento)
                else:
                    if posicoes == (x, y):
                        elementos_na_posicao.append(elemento)

            if elementos_na_posicao:
                # Calcula a posição inicial Y para alinhar os elementos
                y_inicial = y + (tamanho_sala - len(elementos_na_posicao) * 50) // 2  # 50 é a altura da imagem
                for i, elemento in enumerate(elementos_na_posicao):
                    img_rect = elementos[elemento].get_rect()
                    img_rect.topleft = (x, y_inicial + i * img_rect.height)  # Alinha à esquerda e no topo
                    tela.blit(elementos[elemento], img_rect)