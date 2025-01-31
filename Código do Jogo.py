import pygame
import random
import time
import os

pygame.init()

# Definir tamanho da tela
lar = 1200
alt = 720

# Criar janela
screen = pygame.display.set_mode((lar, alt))
pygame.display.set_caption('Sobreviver')

# Carregar imagens
cenarios = ["imagens/cenario_deserto.gif", "imagens/cenario_floresta.gif", "imagens/cenario_neve.jpg"]

# Verificar existência dos arquivos antes de carregar
cenarios = [c for c in cenarios if os.path.exists(c)]
bg = pygame.image.load(cenarios[0]).convert_alpha()
bg = pygame.transform.scale(bg, (lar, alt))

playerImg = pygame.image.load('imagens/soldado.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (145, 145))
playerImg = pygame.transform.rotate(playerImg, -90)

zombie = pygame.image.load('imagens/zombie1.webp').convert_alpha()
zombie = pygame.transform.scale(zombie, (110, 110))

bala = pygame.image.load('imagens/bala.png').convert_alpha()
bala = pygame.transform.scale(bala, (73, 73))
bala = pygame.transform.rotate(bala, -45)

# Definir posições iniciais
pos_player_x = 200
pos_player_y = 570

pos_zombie_x = random.randint(800, 1350)
pos_zombie_y = random.randint(50, 640)

# Posição e estado do tiro
pos_bala_x = -100
pos_bala_y = pos_player_y
velocidade_bala = 5
bala_ativa = False

# Criar retângulos para colisão
player_rect = playerImg.get_rect()
zombie_rect = zombie.get_rect()
bala_rect = bala.get_rect()

# Pontuação
xp = 0
vida = 3

# Fonte para exibir pontuação
fonte = pygame.font.Font(None, 36)

# Velocidade do zombie
velocidade_zombie = random.randint(1, 2)
frequencia_zombies = 1

# Velocidade do fundo
x = 0
velocidade_fundo = 1

rodando = True
escolhendo_item = False
inicio_modo_dificil = 0
modo_dificil = False
velocidade_player = 3

# Função de respawn do zombie
def respawn():
    return [random.randint(800, 1350), random.randint(50, 640), random.randint(1, 2) * frequencia_zombies]

# Loop do jogo
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        if event.type == pygame.KEYDOWN:
            if not escolhendo_item:
                if event.key == pygame.K_SPACE and not bala_ativa:
                    bala_ativa = True
                    pos_bala_x = pos_player_x + 50
                    pos_bala_y = pos_player_y + 40
            else:
                escolha = random.randint(1, 3)
                if escolha == 1:
                    frequencia_zombies = max(1, frequencia_zombies - 1)
                elif escolha == 2:
                    vida += 2
                elif escolha == 3:
                    velocidade_player += 1
                bg = pygame.image.load(random.choice(cenarios)).convert_alpha()
                bg = pygame.transform.scale(bg, (lar, alt))
                escolhendo_item = False

    if xp == 25 and not escolhendo_item:
        escolhendo_item = True

    x -= velocidade_fundo
    rel_x = x % bg.get_rect().width
    
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    screen.blit(bg, (rel_x, 0))

    tecla = pygame.key.get_pressed()
    
    player_rect.topleft = (pos_player_x, pos_player_y)
    bala_rect.topleft = (pos_bala_x, pos_bala_y)
    zombie_rect.topleft = (pos_zombie_x, pos_zombie_y)
    
    if tecla[pygame.K_UP] and pos_player_y > 0:
        pos_player_y -= velocidade_player
    if tecla[pygame.K_DOWN] and pos_player_y < alt - 145:
        pos_player_y += velocidade_player
    if tecla[pygame.K_RIGHT] and pos_player_x < lar - 145:
        pos_player_x += velocidade_player
    if tecla[pygame.K_LEFT] and pos_player_x > 0:
        pos_player_x -= velocidade_player

    pos_zombie_x -= velocidade_zombie
    
    if player_rect.colliderect(zombie_rect) or pos_zombie_x < 60:
        vida -= 1
        pos_zombie_x, pos_zombie_y, velocidade_zombie = respawn()
    
    if bala_ativa and bala_rect.colliderect(zombie_rect):
        xp += 1
        pos_zombie_x, pos_zombie_y, velocidade_zombie = respawn()
        bala_ativa = False

    if pos_zombie_x < -50:
        pos_zombie_x, pos_zombie_y, velocidade_zombie = respawn()

    if bala_ativa:
        pos_bala_x += velocidade_bala
        if pos_bala_x > lar:
            bala_ativa = False

    screen.blit(zombie, (pos_zombie_x, pos_zombie_y))
    if bala_ativa:
        screen.blit(bala, (pos_bala_x, pos_bala_y))
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    texto_xp = fonte.render(f"XP: {xp}", True, (255, 255, 255))
    texto_vida = fonte.render(f"Vida: {vida}", True, (255, 0, 0))
    screen.blit(texto_xp, (20, 20))
    screen.blit(texto_vida, (20, 50))

    if escolhendo_item:
        escolha_texto = fonte.render("Escolha um item...", True, (255, 255, 0))
        screen.blit(escolha_texto, (300, 360))

    if vida <= 0:
        rodando = False
    
    pygame.display.update()

pygame.quit()
