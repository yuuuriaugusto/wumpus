import pygame
import random
import time
 
# Configurações do Pygame
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

# Posições dos elementos
posicoes_elementos = {}

# Classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('images/seta.png')
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x + tamanho_sala // 2 - self.rect.width // 2
        self.rect.y = y + tamanho_sala // 2 - self.rect.height // 2
        self.direcao = 0

    def mover(self):
        if self.direcao == 0:
            self.rect.y -= tamanho_sala
        elif self.direcao == 1:
            self.rect.x += tamanho_sala
        elif self.direcao == 2:
            self.rect.y += tamanho_sala
        elif self.direcao == 3:
            self.rect.x -= tamanho_sala

        # Verifica se o jogador saiu da tela
        if self.rect.left < 0 or self.rect.right > largura_tela or self.rect.top < 0 or self.rect.bottom > altura_tela:
            # Se saiu, desfaz o movimento
            if self.direcao == 0:
                self.rect.y += tamanho_sala
            elif self.direcao == 1:
                self.rect.x -= tamanho_sala
            elif self.direcao == 2:
                self.rect.y -= tamanho_sala
            elif self.direcao == 3:
                self.rect.x += tamanho_sala

    def girar(self, direcao):  # Direção: 1 para direita, -1 para esquerda
        self.direcao = (self.direcao + direcao) % 4
        self.image = pygame.transform.rotate(self.image, -90 * direcao)

# Criação do jogador
jogador = Jogador(0, 0)

class Agente(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load('seta.png')
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x + tamanho_sala // 2 - self.rect.width // 2
        self.rect.y = y + tamanho_sala // 2 - self.rect.height // 2
        self.direcao = 0  # Começa virado para a direita
        self.pontos = 0   # Adiciona o atributo pontos
        self.tem_flecha = True

    def mover(self):
        if self.direcao == 0:
            self.rect.y -= tamanho_sala
        elif self.direcao == 1:
            self.rect.x += tamanho_sala
        elif self.direcao == 2:
            self.rect.y += tamanho_sala
        elif self.direcao == 3:
            self.rect.x -= tamanho_sala

        # Verifica se o jogador saiu da tela
        if self.rect.left < 0 or self.rect.right > largura_tela or self.rect.top < 0 or self.rect.bottom > altura_tela:
            # Se saiu, desfaz o movimento
            if self.direcao == 0:
                self.rect.y += tamanho_sala
            elif self.direcao == 1:
                self.rect.x -= tamanho_sala
            elif self.direcao == 2:
                self.rect.y -= tamanho_sala
            elif self.direcao == 3:
                self.rect.x += tamanho_sala

    def girar(self, direcao):  # Direção: 1 para direita, -1 para esquerda
        self.direcao = (self.direcao + direcao) % 4
        self.image = pygame.transform.rotate(self.image, -90 * direcao)

    def _percepcao(self):
        x, y = self.rect.x // tamanho_sala, self.rect.y // tamanho_sala
        percepcoes = []
        if (x, y) == posicoes_elementos.get('ouro'):
            percepcoes.append('resplendor')
        if (x, y) in posicoes_elementos.get('poco', []):
            percepcoes.append('caiu_no_poco')
        if (x, y) == posicoes_elementos.get('monstro'):
            percepcoes.append('devorado')
        if (x, y) in posicoes_elementos.get('cheiro', []):
            percepcoes.append('cheiro')
        if (x, y) in posicoes_elementos.get('brisa', []):
            percepcoes.append('brisa')
        return percepcoes

    def agir(self):
        percepcoes = self._percepcao()

        if 'caiu_no_poco' in percepcoes or 'devorado' in percepcoes:
            self.pontos -= 1000
            print("Agente Morreu! Pontos:", self.pontos)
            return  # Fim do jogo para o agente

        if 'resplendor' in percepcoes:
            self.pontos += 1000
            print("Agente Pegou o Ouro! Pontos:", self.pontos)
            return  # Fim do jogo para o agente

        if hasattr(self, 'ultimo_tempo_acao') and time.time() - self.ultimo_tempo_acao < 0.8:
            return  # Não age se ainda não passou o tempo
        
        acao = random.choice(['mover', 'girar_esquerda', 'girar_direita'])

        if acao == 'mover':
            self.mover()
            self.pontos -= 1
        elif acao == 'girar_esquerda':
            self.girar(-1)
            self.pontos -= 1
        elif acao == 'girar_direita':
            self.girar(1)
            self.pontos -= 1

        self.ultimo_tempo_acao = time.time()

# Distribuição aleatória dos elementos
def distribuir_elementos():
    global posicoes_elementos
    posicoes_elementos = {}

    posicoes_pocos = []
    for x in range(0, largura_tela, tamanho_sala):
        for y in range(0, altura_tela, tamanho_sala):
            if (x, y) != (0, 0) and random.random() < 0.1:  # 10% de chance
                posicoes_pocos.append((x, y))
    posicoes_elementos['poco'] = posicoes_pocos

    # Posicionando os outros elementos
    for elemento in ['monstro', 'ouro']:
        while True:
            x = random.randrange(0, largura_tela, tamanho_sala)
            y = random.randrange(0, altura_tela, tamanho_sala)
            if (x, y) != (0, 0) and (x, y) not in posicoes_pocos:
                break
        posicoes_elementos[elemento] = (x, y)

    # Posicionando as brisas (adjacentes aos poços, mas não sobre eles)
    posicoes_brisas = []
    for x, y in posicoes_pocos:
        for dx, dy in [(0, -tamanho_sala), (tamanho_sala, 0), (0, tamanho_sala), (-tamanho_sala, 0)]:
            nova_pos = (x + dx, y + dy)
            if 0 <= nova_pos[0] < largura_tela and 0 <= nova_pos[1] < altura_tela and nova_pos not in posicoes_pocos:
                posicoes_brisas.append(nova_pos)
    posicoes_elementos['brisa'] = posicoes_brisas

    # Posicionando os cheiros (adjacentes ao monstro, mas não sobre ele)
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

# Loop principal do jogo
rodando = True
distribuir_elementos()
agente = None
jogador_ativo = True
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
                agente = Agente(0, 0)
                jogador_ativo = False

    # Agente age (se existir)
    if agente is not None:
        agente.agir()

    # Desenho do cenário, jogador e agente
    desenhar_cenario()
    if jogador_ativo: 
        tela.blit(jogador.image, jogador.rect)
    
    if agente is not None:
        tela.blit(agente.image, agente.rect)

    pygame.display.flip()

pygame.quit()
