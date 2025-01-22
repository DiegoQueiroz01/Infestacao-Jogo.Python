import pygame

pygame.init()

x=1200
y=720

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('Sobreviver')

rodando = True

while rodando:
    for event in pygame.event.get():
        if event.type - pygame.QUIT:
            rodando = False
    pygame.display.update()