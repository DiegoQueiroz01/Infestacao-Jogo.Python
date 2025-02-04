import pygame
import random

pygame.init()

# Configurações da tela
lar, alt = 800, 600
screen = pygame.display.set_mode((lar, alt))
pygame.display.set_caption('Sobreviver')

# Carregar imagens dos cenários
cenarios = {
    1: 'Imagens/cenario_floresta.gif',
    2: 'Imagens/cenario_neve.jpg',
    3: 'Imagens/cenario_deserto.gif'
}

class Player:
    def __init__(self):
        self.image = pygame.image.load('Imagens/soldado.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.image = pygame.transform.flip(self.image, True, True)
        self.image = pygame.transform.rotate(self.image, 90)
        self.x = 200
        self.y = 570
        self.velocidade = 2
        self.vida = 6
        self.tiro_rapido = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Zombie:
    def __init__(self):
        self.image = pygame.image.load('Imagens/zombie1.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.respawn()

    def respawn(self):
        self.x = random.randint(800, 1350)
        self.y = random.randint(50, alt - 80)
        self.velocidade = 1

    def update(self):
        self.x -= self.velocidade
        if self.x < -80:
            self.respawn()
            player.vida -= 1  # Perde vida quando o zumbi passa

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
zombie = Zombie()
bala = Bala()
cenario_atual = 3  # Padrão deserto
bg = pygame.image.load(cenarios[cenario_atual]).convert_alpha()
bg = pygame.transform.scale(bg, (lar, alt))

xp = 0
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
                pausado = True
                while pausado:
                    screen.fill((0, 0, 0))
                    texto = fonte.render("Escolha uma opção:", True, (255, 255, 255))
                    option1 = fonte.render("1 - Mais Velocidade", True, (255, 255, 255))
                    option2 = fonte.render("2 - Mais Vida", True, (255, 255, 255))
                    option3 = fonte.render("3 - Tiro Mais Rápido", True, (255, 255, 255))
                    screen.blit(texto, (lar // 2 - texto.get_width() // 2, alt // 2 - 80))
                    screen.blit(option1, (lar // 2 - option1.get_width() // 2, alt // 2 - 40))
                    screen.blit(option2, (lar // 2 - option2.get_width() // 2, alt // 2))
                    screen.blit(option3, (lar // 2 - option3.get_width() // 2, alt // 2 + 40))
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pausado = False
                            rodando = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                player.velocidade += 1
                                zombie.velocidade += 1
                                cenario_atual = 1
                            elif event.key == pygame.K_2:
                                player.vida += 3
                                cenario_atual = 2
                            elif event.key == pygame.K_3:
                                player.tiro_rapido = True
                                cenario_atual = 3
                            pausado = False
                            xp = 0

    bg = pygame.image.load(cenarios[cenario_atual]).convert_alpha()
    bg = pygame.transform.scale(bg, (lar, alt))

    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and player.y > 0:
        player.y -= player.velocidade
    if tecla[pygame.K_DOWN] and player.y < alt - 80:
        player.y += player.velocidade
    if tecla[pygame.K_RIGHT] and player.x < lar - 80:
        player.x += player.velocidade
    if tecla[pygame.K_LEFT] and player.x > 0:
        player.x -= player.velocidade

    bala.update()
    zombie.update()

    bala_rect = pygame.Rect(bala.x, bala.y, 30, 30)
    zombie_rect = pygame.Rect(zombie.x, zombie.y, 80, 80)

    if bala.ativa and bala_rect.colliderect(zombie_rect):
        xp += 1
        bala.ativa = False
        zombie.respawn()

    player_rect = pygame.Rect(player.x, player.y, 80, 80)
    if player_rect.colliderect(zombie_rect):
        player.vida -= 1
        zombie.respawn()
    
    if player.vida <= 0:
        rodando = False

    x -= 1
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    screen.blit(bg, (rel_x, 0))

    zombie.draw(screen)
    bala.draw(screen)
    player.draw(screen)

    screen.blit(fonte.render(f"XP: {xp}", True, (255, 255, 255)), (20, 20))
    screen.blit(fonte.render(f"Vida: {player.vida}", True, (255, 0, 0)), (20, 50))
    pygame.display.update()

pygame.quit()
