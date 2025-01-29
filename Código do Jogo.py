import pygame
import random

pygame.init()

# Definir tamanho da tela
lar = 1200
alt = 720

# Criar janela
screen = pygame.display.set_mode((lar, alt))
pygame.display.set_caption('Sobreviver')

# Carregar imagens
bg = pygame.image.load('imagens/cenário01.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (lar, alt))

playerImg = pygame.image.load('imagens/soldado.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (145, 145))
playerImg = pygame.transform.rotate(playerImg, -90)

zombie = pygame.image.load('imagens/zombie.png').convert_alpha()
zombie = pygame.transform.scale(zombie, (110, 110))

bala = pygame.image.load('imagens/bala.png').convert_alpha()
bala = pygame.transform.scale(bala, (73, 73))
bala = pygame.transform.rotate(bala, -45)

# Definir posições iniciais
pos_player_x = 200
pos_player_y = 570

pos_zombie_x = random.randint(800, 1350)  # zombie começa em qualquer lugar da direita
pos_zombie_y = random.randint(50, 640)

# Posição e estado do tiro
pos_bala_x = -100  # Começa fora da tela
pos_bala_y = pos_player_y
velocidade_bala = 5
bala_ativa = False  # A bala só aparece quando atirar

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
velocidade_zombie = random.randint(1, 2)  # Cada zombie pode ter uma velocidade diferente

# Velocidade do fundo
x = 0
velocidade_fundo = 1

rodando = True

# Função de respawn do zombie
def respawn():
    return [random.randint(800, 1350), random.randint(50, 640), random.randint(1, 2)]  # Retorna também a velocidade

# Loop do jogo
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        # Disparo do tiro (tecla espaço)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bala_ativa:
                bala_ativa = True
                pos_bala_x = pos_player_x + 50  # Posição inicial do tiro ao lado do soldado
                pos_bala_y = pos_player_y + 40

    # Movimentação do fundo
    x -= velocidade_fundo
    rel_x = x % bg.get_rect().width

    # Limpar a tela e redesenhar o fundo
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    screen.blit(bg, (rel_x, 0))

    # Teclas de comando
    tecla = pygame.key.get_pressed()
    
    # Atualizar posições dos retângulos
    player_rect.topleft = (pos_player_x, pos_player_y)
    bala_rect.topleft = (pos_bala_x, pos_bala_y)
    zombie_rect.topleft = (pos_zombie_x, pos_zombie_y)

    # Movimentação do jogador
    if tecla[pygame.K_UP] and pos_player_y > 0:
        pos_player_y -= 3
    if tecla[pygame.K_DOWN] and pos_player_y < alt - 145:  # Limite inferior
        pos_player_y += 3
    if tecla[pygame.K_RIGHT] and pos_player_x < lar - 145:  # Limite direito
        pos_player_x += 3
    if tecla[pygame.K_LEFT] and pos_player_x > 0:  # Limite esquerdo
        pos_player_x -= 3

    # Movimentação do zombie
    pos_zombie_x -= velocidade_zombie  

    # Verificar se o zombie tocou o jogador ou passou por ele
    if player_rect.colliderect(zombie_rect) or pos_zombie_x < 60:
        vida -= 1  # Perde 1 de vida
        pos_zombie_x, pos_zombie_y, velocidade_zombie = respawn()  # Respawn do zumbi

    # Verificar se o tiro acertou o zumbi
    if bala_ativa and bala_rect.colliderect(zombie_rect):
        xp += 1  # Ganha 1 de XP
        pos_zombie_x, pos_zombie_y, velocidade_zombie = respawn()  # Respawn do zumbi
        bala_ativa = False  # Resetar a bala

    # Respawn do zombie em posição aleatória se ele sair da tela
    if pos_zombie_x < -50:
        pos_zombie_x, pos_zombie_y, velocidade_zombie = respawn()

    # Movimentação do tiro
    if bala_ativa:
        pos_bala_x += velocidade_bala
        if pos_bala_x > lar:  # Se sair da tela, reseta
            bala_ativa = False

    # Desenhar imagens
    screen.blit(zombie, (pos_zombie_x, pos_zombie_y))
    if bala_ativa:
        screen.blit(bala, (pos_bala_x, pos_bala_y))  # Renderiza o tiro apenas se ativo
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    # Exibir XP e Vida
    texto_xp = fonte.render(f"XP: {xp}", True, (255, 255, 255))
    texto_vida = fonte.render(f"Vida: {vida}", True, (255, 0, 0))
    screen.blit(texto_xp, (20, 20))
    screen.blit(texto_vida, (20, 50))

    # Fim de jogo se a vida chegar a 0
    if vida <= 0:
        rodando = False

    pygame.display.update()

pygame.quit()