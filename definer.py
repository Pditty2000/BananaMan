import pygame
import sys
import json


pygame.init()
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 64)
user_text = ''
screen = pygame.display.set_mode((800, 600))
screen_text = 'Enter Word:'
input_box = pygame.Rect(200, 200, 140, 45)

color_active = (255,255,255)
color_inactive = (255,0,0)

active = False
playing = True
while playing:
    word = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # Check for backspace 
            if event.key == pygame.K_BACKSPACE: 
                user_text = user_text[:-1] 
            # check for Return
            if event.key == pygame.K_RETURN:
                word = user_text
            # Unicode standard is used for string 
            # formation 
            else: 
                user_text += event.unicode

    if active:
        color = color_active
    else:
        color = color_inactive
    
    screen.fill((255,255,255))
    pygame.draw.rect(screen, color, input_box)

    text_surface = FONT.render(user_text, True, (0,0,0))
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    input_box.w = max(100, text_surface.get_width()+10) 
    input_box.h = max(45, text_surface.get_height()+5)

    
    pygame.display.flip()
    clock.tick(60)