import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
screen.fill((255,255,255))

FONT = pygame.font.Font(None, 64)

done = False
limit = 10000
while not done:
    screen.fill((255,255,255))
    limit_text = FONT.render(f'limit: {limit}', True, (0,255,0))
    if limit <= 0:
        done = True
    print(f'running: {limit}')
    screen.blit(limit_text, (screen.get_width()/2, screen.get_height()/2))
    limit -= 1
    pygame.display.flip()


