# main.py
import pygame
import random
import time

pygame.init()
largura_tela = 600
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Mundo de Wumpus")

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)

# Tamanho da sala
tamanho_sala = 150

# Elementos do jogo
elementos = {
    'monstro': pygame.transform.scale(pygame.image.load('images/monstro.png'), (50, 50)),
    'ouro': pygame.transform.scale(pygame.image.load('images/ouro.png'), (50, 50)),
    'poco': pygame.transform.scale(pygame.image.load('images/poco.png'), (50, 50)),
    'cheiro': pygame.transform.scale(pygame.image.load('images/cheiro.png'), (50, 50)),
    'brisa': pygame.transform.scale(pygame.image.load('images/brisa.png'), (50, 50))
}

posicoes_elementos = {}

def distribuir_elementos():
    global posicoes_elementos
    posicoes_elementos = {}

    posicoes_pocos = []
    for x in range(0, largura_tela - tamanho_sala, tamanho_sala):  # Ajustar intervalo do x
        for y in range(0, altura_tela - tamanho_sala, tamanho_sala):  # Ajustar intervalo do y
            if (x, y) != (0, 0) and random.random() < 0.1:  
                posicoes_pocos.append((x, y))
    posicoes_elementos['poco'] = posicoes_pocos

    for elemento in ['monstro', 'ouro']:
        while True:
            x = random.randrange(0, largura_tela - tamanho_sala, tamanho_sala)  # Ajustar intervalo do x
            y = random.randrange(0, altura_tela - tamanho_sala, tamanho_sala)  # Ajustar intervalo do y
            if (x, y) != (0, 0) and (x, y) not in posicoes_pocos:
                break
        posicoes_elementos[elemento] = (x, y)

    posicoes_brisas = []
    for x, y in posicoes_pocos:
        for dx, dy in [(0, -tamanho_sala), (tamanho_sala, 0), (0, tamanho_sala), (-tamanho_sala, 0)]:
            nova_pos = (x + dx, y + dy)
            if 0 <= nova_pos[0] < largura_tela and 0 <= nova_pos[1] < altura_tela and nova_pos not in posicoes_pocos:
                posicoes_brisas.append(nova_pos)
    posicoes_elementos['brisa'] = posicoes_brisas

    x, y = posicoes_elementos['monstro']
    posicoes_cheiros = []
    for dx, dy in [(0, -tamanho_sala), (tamanho_sala, 0), (0, tamanho_sala), (-tamanho_sala, 0)]:
        nova_pos = (x + dx, y + dy)
        if 0 <= nova_pos[0] < largura_tela and 0 <= nova_pos[1] < altura_tela and nova_pos != (x, y):
            posicoes_cheiros.append(nova_pos)
    posicoes_elementos['cheiro'] = posicoes_cheiros

def desenhar_cenario():
    tela.fill(preto)
    for x in range(0, largura_tela, tamanho_sala):
        for y in range(0, altura_tela, tamanho_sala):
            pygame.draw.rect(tela, branco, (x, y, tamanho_sala, tamanho_sala))
            pygame.draw.rect(tela, preto, (x, y, tamanho_sala, tamanho_sala), 2)

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

def main():
    global posicoes_elementos
    from jogador import Jogador
    from agente import Agente

    rodando = True
    distribuir_elementos()
    jogador = Jogador(0, 0, largura_tela, altura_tela)
    agente = None
    jogador_ativo = True

    print(posicoes_elementos)

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    jogador.mover()
                if evento.key == pygame.K_RIGHT:
                    jogador.girar(1)
                if evento.key == pygame.K_LEFT:
                    jogador.girar(-1)
                if evento.key == pygame.K_SPACE and agente is None:  
                    agente = Agente(0, 0, largura_tela, altura_tela, posicoes_elementos)
                    jogador_ativo = False

        if agente is not None:
            info = agente.agir()

            if info == 'terminar':
                rodando = False

        desenhar_cenario()
        if jogador_ativo: 
            tela.blit(jogador.image, jogador.rect)
        
        if agente is not None:
            tela.blit(agente.image, agente.rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()