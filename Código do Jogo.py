import pygame
import random
import time

pygame.init()

# Configurações da tela
lar, alt = 800, 600
screen = pygame.display.set_mode((lar, alt))
pygame.display.set_caption('Sobreviver')

# Carregar imagens dos cenários
cenarios = {
    1: 'Imagens/cenario_deserto.gif',
    2: 'Imagens/cenario_neve.jpg',
    3: 'Imagens/cenario_floresta.gif'
}

class Player:
    def __init__(self):
        self.image = pygame.image.load('Imagens/soldado.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.image = pygame.transform.flip(self.image, True, True)  # Virado para a esquerda
        self.image = pygame.transform.rotate(self.image, 90) #Muda o ângulo do eixo vertical
        self.x = 200
        self.y = 570
        self.velocidade = 2  # Velocidade reduzida para 2
        self.vida = 6

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Zombie:
    def __init__(self):
        self.image = pygame.image.load('Imagens/zombie1.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  # Mesmo tamanho do soldado
        self.respawn()

    def respawn(self):
        self.x = random.randint(800, 1350)
        self.y = random.randint(50, alt - 80)
        self.velocidade = 1  # Velocidade reduzida para 1
    
    def update(self):
        self.x -= self.velocidade
        if self.x < -80:  # Saiu da tela, reaparece
            self.respawn()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bala:
    def __init__(self):
        self.image = pygame.image.load('Imagens/bala.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image = pygame.transform.rotate(self.image, -45)
        self.x = -100
        self.y = 0
        self.velocidade = 7
        self.ativa = False
    
    def update(self):
        if self.ativa:
            self.x += self.velocidade
            if self.x > lar:  # Saiu da tela, desativa
                self.ativa = False

    def draw(self, screen):
        if self.ativa:
            screen.blit(self.image, (self.x, self.y))

# Inicializar objetos
player = Player()
zombie = Zombie()
bala = Bala()

# Carregar o cenário inicial
cenario_atual = 1
bg = pygame.image.load(cenarios[cenario_atual]).convert_alpha()
bg = pygame.transform.scale(bg, (lar, alt))

# Pontuação e vida
xp = 0
fonte = pygame.font.Font(None, 36)
x = 0
rodando = True

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bala.ativa:
                bala.ativa = True
                bala.x, bala.y = player.x + 50, player.y + 40

    # Movimentação do jogador
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and player.y > 0:
        player.y -= player.velocidade
    if tecla[pygame.K_DOWN] and player.y < alt - 80:
        player.y += player.velocidade
    if tecla[pygame.K_RIGHT] and player.x < lar - 80:
        player.x += player.velocidade
    if tecla[pygame.K_LEFT] and player.x > 0:
        player.x -= player.velocidade

    # Atualizar posição da bala e do zumbi
    bala.update()
    zombie.update()

    # Checar colisão da bala com o zumbi
    bala_rect = pygame.Rect(bala.x, bala.y, 30, 30)
    zombie_rect = pygame.Rect(zombie.x, zombie.y, 80, 80)

    if bala.ativa and bala_rect.colliderect(zombie_rect):
        xp += 1
        bala.ativa = False
        zombie.respawn()

    # Checar colisão do zumbi com o jogador
    player_rect = pygame.Rect(player.x, player.y, 80, 80)
    if player_rect.colliderect(zombie_rect):
        player.vida -= 1
        zombie.respawn()
    
    # Se a vida chegar a 0, o jogo acaba
    if player.vida <= 0:
        rodando = False

    # Desenhar elementos na tela
    x -= 1
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    screen.blit(bg, (rel_x, 0))

    zombie.draw(screen)
    bala.draw(screen)
    player.draw(screen)

    texto_xp = fonte.render(f"XP: {xp}", True, (255, 255, 255))
    texto_vida = fonte.render(f"Vida: {player.vida}", True, (255, 0, 0))
    screen.blit(texto_xp, (20, 20))
    screen.blit(texto_vida, (20, 50))

    pygame.display.update()

pygame.quit()