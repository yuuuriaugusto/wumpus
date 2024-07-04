# jogador.py
import pygame

# Tamanho da sala (importado do main.py ou definido como global)
tamanho_sala = 150

class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y, largura_tela, altura_tela):
        super().__init__()
        self.original_image = pygame.image.load('images/seta.png')
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x + tamanho_sala // 2 - self.rect.width // 2
        self.rect.y = y + tamanho_sala // 2 - self.rect.height // 2
        self.direcao = 0
        self.largura_tela = largura_tela  # Armazena como atributo da classe
        self.altura_tela = altura_tela

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
        if self.rect.left < 0 or self.rect.right > self.largura_tela or self.rect.top < 0 or self.rect.bottom > self.altura_tela:
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
