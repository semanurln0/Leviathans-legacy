import pygame

pygame.init()


info = pygame.display.Info()
w = info.current_w
h = info.current_h -50

screen = pygame.display.set_mode((w, h), pygame.SCALED | pygame.RESIZABLE)
screen.fill((255, 255, 255))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
