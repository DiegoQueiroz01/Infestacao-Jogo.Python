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
        self.x = 200
        self.y = 570
        self.velocidade = 2  # Velocidade inicial do jogador
        self.vida = 6
        self.tiro_rapido = False  # Controla se o tiro é rápido ou não

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Zombie:
    def __init__(self, resistencia=1):
        self.image = pygame.image.load('Imagens/zombie1.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.resistencia = resistencia
        self.respawn()

    def respawn(self):
        self.x = random.randint(800, 1350)
        self.y = random.randint(50, alt - 80)
        self.velocidade = 1
        self.vida = self.resistencia
    
    def update(self):
        self.x -= self.velocidade
        if self.x < -80:
            player.vida -= 1
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
            if self.x > lar:
                self.ativa = False

    def draw(self, screen):
        if self.ativa:
            screen.blit(self.image, (self.x, self.y))

player = Player()
zombies = [Zombie()]
bala = Bala()

cenario_atual = 1
bg = pygame.image.load(cenarios[cenario_atual]).convert_alpha()
bg = pygame.transform.scale(bg, (lar, alt))

xp = 0
total_xp = 0
fonte = pygame.font.Font(None, 36)
x = 0
rodando = True
pausado = False

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bala.ativa:
                bala.ativa = True
                bala.x, bala.y = player.x + 50, player.y + 40

            if xp >= 15 and not pausado:
                total_xp += xp
                pausado = True
                while pausado:
                    screen.fill((0, 0, 0))
                    option1 = fonte.render("1 - Mais Velocidade", True, (255, 255, 255))
                    option2 = fonte.render("2 - Mais Vida", True, (255, 255, 255))
                    option3 = fonte.render("3 - Tiro Mais Rápido", True, (255, 255, 255))
                    screen.blit(option1, (200, 200))
                    screen.blit(option2, (200, 250))
                    screen.blit(option3, (200, 300))
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pausado = False
                            rodando = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                player.velocidade += 1
                                zombies = [Zombie() for _ in range(2)]
                            elif event.key == pygame.K_2:
                                player.vida += 3
                                zombies = [Zombie(resistencia=2)]
                            elif event.key == pygame.K_3:
                                player.tiro_rapido = True
                                zombies = [Zombie(resistencia=3)]
                            cenario_atual = random.choice(list(cenarios.keys()))
                            pausado = False
                            xp = 0

    bg = pygame.image.load(cenarios[cenario_atual]).convert_alpha()
    bg = pygame.transform.scale(bg, (lar, alt))

    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and player.y > 0:
        player.y -= player.velocidade
    if tecla[pygame.K_DOWN] and player.y < alt - 80:
        player.y += player.velocidade
    if tecla[pygame.K_LEFT] and player.x > 0:
        player.x -= player.velocidade
    if tecla[pygame.K_RIGHT] and player.x < lar - 80:
        player.x += player.velocidade

    bala.update()
    for zombie in zombies:
        zombie.update()
        bala_rect = pygame.Rect(bala.x, bala.y, 30, 30)
        zombie_rect = pygame.Rect(zombie.x, zombie.y, 80, 80)
        if bala.ativa and bala_rect.colliderect(zombie_rect):
            zombie.vida -= 1
            if zombie.vida <= 0:
                xp += 1
                zombie.respawn()
            bala.ativa = False

    if player.vida <= 0:
        rodando = False

    x -= 1
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    screen.blit(bg, (rel_x, 0))

    for zombie in zombies:
        zombie.draw(screen)
    bala.draw(screen)
    player.draw(screen)
    screen.blit(fonte.render(f"XP: {total_xp}", True, (255, 255, 255)), (20, 20))
    screen.blit(fonte.render(f"Vida: {player.vida}", True, (255, 0, 0)), (20, 50))
    pygame.display.update()

pygame.quit()

