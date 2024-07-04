import pygame
import random
import time

from main import tamanho_sala

class Agente(pygame.sprite.Sprite):
    def __init__(self, x, y, largura_tela, altura_tela, posicoes_elementos):
        super().__init__()
        self.original_image = pygame.image.load('images/seta.png')
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x + tamanho_sala // 2 - self.rect.width // 2
        self.rect.y = y + tamanho_sala // 2 - self.rect.height // 2
        self.direcao = 0
        self.pontos = 0
        self.tem_flecha = True
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.mapa = [['?' for _ in range(largura_tela // tamanho_sala)] for _ in range(altura_tela // tamanho_sala)]
        self.mapa[self.rect.y // tamanho_sala][self.rect.x // tamanho_sala] = 'S'  # Posição inicial
        self.visitados = set()
        self.wumpus_morto = False
        # self.percepcao_atual = []
        self.posicoes_elementos = posicoes_elementos
        self.percepcao_atual = self._percepcao()

    def imprimir_mapa(self):
        """Imprime o mapa na tela."""
        print("-" * 20)
        for linha in self.mapa:
            print("  ".join(linha))
        print("-" * 20) 

    def mover(self):
        self.pontos -= 1 

        if self.direcao == 0:
            self.rect.y -= tamanho_sala
        elif self.direcao == 1:
            self.rect.x += tamanho_sala
        elif self.direcao == 2:
            self.rect.y += tamanho_sala
        elif self.direcao == 3:
            self.rect.x -= tamanho_sala

        self.rect.x = max(0, min(self.rect.x, self.largura_tela - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.altura_tela - self.rect.height))

        self.rect.x = (self.rect.x // tamanho_sala) * tamanho_sala + tamanho_sala // 2 - self.rect.width // 2
        self.rect.y = (self.rect.y // tamanho_sala) * tamanho_sala + tamanho_sala // 2 - self.rect.height // 2

        self.percepcao_atual = self._percepcao()
        self.atualizar_mapa()
        self.imprimir_mapa()

        if 'caiu_no_poco' in self.percepcao_atual or 'devorado' in self.percepcao_atual:
            self.pontos -= 1000
            print("Agente Morreu! Pontos:", self.pontos)
            return 'terminar'  
        elif 'resplendor' in self.percepcao_atual:
            self.pontos += 1000
            print("Agente Pegou o Ouro! Pontos:", self.pontos)
            return 'terminar' 

    def girar(self, direcao):
        self.direcao = (self.direcao + direcao) % 4
        self.image = pygame.transform.rotate(self.image, -90 * direcao)
        self.pontos -= 1

    def atirar_flecha(self):
        if self.tem_flecha:
            self.tem_flecha = False
            self.pontos -= 10
            x, y = self.rect.x // tamanho_sala, self.rect.y // tamanho_sala

            if self.direcao == 0:  # Cima
                for i in range(y - 1, -1, -1):
                    if self.mapa[i][x] == 'W':
                        self.wumpus_morto = True
                        self.mapa[i][x] = '?'
                        print("WUMPUS MORTO! Você ouviu um grito distante.")
                        break  # Para após matar o Wumpus
            elif self.direcao == 1:  # Direita
                for i in range(x + 1, len(self.mapa[0])):
                    if self.mapa[y][i] == 'W':
                        self.wumpus_morto = True
                        self.mapa[y][i] = '?'
                        print("WUMPUS MORTO! Você ouviu um grito distante.")
                        break
            elif self.direcao == 2:  # Baixo
                for i in range(y + 1, len(self.mapa)):
                    if self.mapa[i][x] == 'W':
                        self.wumpus_morto = True
                        self.mapa[i][x] = '?'
                        print("WUMPUS MORTO! Você ouviu um grito distante.")
                        break
            elif self.direcao == 3:  # Esquerda
                for i in range(x - 1, -1, -1):
                    if self.mapa[y][i] == 'W':
                        self.wumpus_morto = True
                        self.mapa[y][i] = '?'
                        print("WUMPUS MORTO! Você ouviu um grito distante.")
                        break

    def _percepcao(self):
        x = self.rect.x // tamanho_sala
        y = self.rect.y // tamanho_sala
        percepcoes = []

        print("Posição do Agente:", x, y) 

        if (x * tamanho_sala, y * tamanho_sala) == self.posicoes_elementos.get('ouro'):
            percepcoes.append('resplendor')
        if (x * tamanho_sala, y * tamanho_sala) in self.posicoes_elementos.get('poco', []):
            percepcoes.append('caiu_no_poco')
        if (x * tamanho_sala, y * tamanho_sala) == self.posicoes_elementos.get('monstro') and not self.wumpus_morto:
            percepcoes.append('devorado')
        if (x * tamanho_sala, y * tamanho_sala) in self.posicoes_elementos.get('cheiro', []):
            percepcoes.append('cheiro')
        if (x * tamanho_sala, y * tamanho_sala) in self.posicoes_elementos.get('brisa', []):
            percepcoes.append('brisa')

        print("Percepções:", percepcoes)
        return percepcoes
    
    def atualizar_mapa(self):
        x, y = self.rect.x // tamanho_sala, self.rect.y // tamanho_sala

        if 'caiu_no_poco' in self.percepcao_atual:
            self.mapa[y][x] = 'P'
        elif 'devorado' in self.percepcao_atual:
            self.mapa[y][x] = 'W' 
        else:  
            self.mapa[y][x] = 'S'  

        self.visitados.add((x, y))

        if 'brisa' in self.percepcao_atual:
            self.marcar_adjacentes(x, y, 'P?') 
        if 'cheiro' in self.percepcao_atual:
            self.marcar_adjacentes(x, y, 'W?')

    def marcar_adjacentes(self, x, y, marca):
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.mapa[0]) and 0 <= ny < len(self.mapa) and self.mapa[ny][nx] == '?':
                self.mapa[ny][nx] = marca

    def escolher_acao(self):
        if 'resplendor' in self.percepcao_atual:
            self.pontos += 1000
            print("Agente Pegou o Ouro! Pontos:", self.pontos)
            return 'terminar'  
        
        x, y = self.rect.x // tamanho_sala, self.rect.y // tamanho_sala
        self.deduzir_wumpus()

        casas_seguras = self.obter_casas_adjacentes('S', x, y) 
        for nx, ny in casas_seguras:
            if (nx, ny) not in self.visitados:
                return self.mover_para_celula(nx, ny)

        if self.tem_flecha:
            if self.avaliar_tiro(x, y):
                return 'atirar_flecha'

        casas_desconhecidas = self.obter_casas_adjacentes('?', x, y)
        if casas_desconhecidas:
            nx, ny = random.choice(casas_desconhecidas)
            return self.mover_para_celula(nx, ny)

        casas_seguras_visitadas = self.obter_casas_adjacentes('S', x, y, visitados=True)
        if casas_seguras_visitadas:
            nx, ny = random.choice(casas_seguras_visitadas)
            return self.mover_para_celula(nx, ny)

        return random.choice(['girar_esquerda', 'girar_direita'])

    def deduzir_wumpus(self):
        """Deduz a posição do Wumpus com base em pares de cheiros e células seguras."""
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[0])):
                if (x * tamanho_sala, y * tamanho_sala) in self.posicoes_elementos.get('cheiro', []):
                    # 1. Verificar se há outro cheiro adjacente
                    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(self.mapa[0]) and 0 <= ny < len(self.mapa) and \
                           (nx * tamanho_sala, ny * tamanho_sala) in self.posicoes_elementos.get('cheiro', []):
                            
                            x_atras = x - dx
                            y_atras = y - dy
                            nx_atras = nx - dx
                            ny_atras = ny - dy

                            if 0 <= x_atras < len(self.mapa[0]) and 0 <= y_atras < len(self.mapa) and \
                               self.mapa[y_atras][x_atras] == 'S':
                                self.mapa[y][x] = 'W' 
                                self.wumpus_morto = True
                                self.limpar_possiveis_wumpus()
                                return

                            if 0 <= nx_atras < len(self.mapa[0]) and 0 <= ny_atras < len(self.mapa) and \
                               self.mapa[ny_atras][nx_atras] == 'S':
                                self.mapa[ny][nx] = 'W' 
                                self.wumpus_morto = True
                                self.limpar_possiveis_wumpus()
                                return
                            
    def limpar_possiveis_wumpus(self):
        """Marca todas as células 'W?' como 'S'."""
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[0])):
                if self.mapa[y][x] == 'W?':
                    self.mapa[y][x] = 'S'

    def obter_casas_adjacentes(self, tipo, x, y, visitados=False):
        """Retorna uma lista de casas adjacentes do tipo especificado."""
        casas = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.mapa[0]) and 0 <= ny < len(self.mapa):
                if visitados and (nx, ny) in self.visitados and self.mapa[ny][nx] == tipo:
                    casas.append((nx, ny))
                elif not visitados and self.mapa[ny][nx] == tipo:
                    casas.append((nx, ny))
        return casas

    def mover_para_celula(self, nx, ny):
        """Move o agente para a célula especificada, evitando giros desnecessários."""
        x, y = self.rect.x // tamanho_sala, self.rect.y // tamanho_sala

        if nx > x and self.direcao != 1 and self.rect.right < self.largura_tela:  
            return 'girar_direita'
        elif nx < x and self.direcao != 3 and self.rect.left > 0: 
            return 'girar_esquerda'
        elif ny > y and self.direcao != 2 and self.rect.bottom < self.altura_tela:  
            return 'girar_direita'
        elif ny < y and self.direcao != 0 and self.rect.top > 0:  
            return 'girar_esquerda'
        else:
            return 'mover'

    def avaliar_tiro(self, x, y):
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.mapa[0]) and 0 <= ny < len(self.mapa) and self.mapa[ny][nx] == 'W?':
                return True 

        return False
    
    def agir(self):
        if hasattr(self, 'ultimo_tempo_acao') and time.time() - self.ultimo_tempo_acao < 0.6:
            return

        self.percepcao_atual = self._percepcao() 

        if 'caiu_no_poco' in self.percepcao_atual or 'devorado' in self.percepcao_atual:
            self.pontos -= 1000
            print("Agente Morreu! Pontos:", self.pontos)
            self.atualizar_mapa() 
            self.imprimir_mapa()
            return 'terminar'  
        elif 'resplendor' in self.percepcao_atual:
            self.pontos += 1000
            print("Agente Pegou o Ouro! Pontos:", self.pontos)
            self.atualizar_mapa()
            self.imprimir_mapa()
            return 'terminar' 

        acao = self.escolher_acao() 

        if acao == 'mover':
            info = self.mover() 

            if info == 'terminar':
                return 'terminar'
        elif acao == 'girar_esquerda':
            self.girar(-1)
        elif acao == 'girar_direita':
            self.girar(1)
        elif acao == 'atirar_flecha':
            self.atirar_flecha()

        self.ultimo_tempo_acao = time.time()