import pygame #importar biblioteca do pygame

pygame.init() #inicializar o pygame

#definir tamanho da tela do jogo
lar=1200
alt=720

#tornar com que a janela apareça ao rodar o código
screen = pygame.display.set_mode((lar,alt))
pygame.display.set_caption('Sobreviver')

#definir cenário da imagem
bg = pygame.image.load('imagens/cenário01.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (lar,alt))

#definir player
playerImg = pygame.image.load('imagens/soldado.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (145,145)) #define o tamanho do soldado
playerImg = pygame.transform.rotate(playerImg, -90)

#definir zombies
zombie = pygame.image.load('imagens/zombie.png').convert_alpha()
zombie = pygame.transform.scale(zombie, (110,110)) #define o tamanho do zombie

#definir posiçoes iniciais
pos_player_x = 200
pos_player_y = 570

pos_zombie_x = 500
pos_zombie_y = 620

#iniciar a posição do cenário de fundo
x = 0
velocidade = 1

rodando = True

#criar loop para manter a tela rodando
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    x-= velocidade
    rel_x = x % bg.get_rect().width

    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    screen.blit(bg, (rel_x, 0))

    screen.blit(zombie, (pos_zombie_y, pos_zombie_y))
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    #teclas de comando
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_RIGHT] and pos_player_x < 1000:
        pos_player_x += 1
    if tecla[pygame.K_LEFT] and pos_player_x > 1:
        pos_player_x -= 1
    
    pygame.display.update()
pygame.quit()