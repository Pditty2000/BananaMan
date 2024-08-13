import pygame
import random

pygame.init()
# BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
ERROR_IMAGE = 'Images/error.png'
BACKGROUND_COLOR = (0,255,0)
TEXT_COLOR = (0,0,0)
TITLE_TEXT = 'BananaMan!'
TITLE_FONT = pygame.font.Font(None, 64)
INSTRUCTION_TEXT = 'Press SPACE to begin...'
INSTRUCTION_FONT = pygame.font.Font(None, 32)

# splash_image = pygame.image.load(BACKGROUND_IMAGE)
# splash_image = pygame.transform.scale(splash_image, (1080, 606))

error_image = pygame.image.load(ERROR_IMAGE)
error_image = pygame.transform.scale(error_image, (606, 606))
splash_title = TITLE_FONT.render(TITLE_TEXT, True, TEXT_COLOR)
instructions = INSTRUCTION_FONT.render(INSTRUCTION_TEXT, True, TEXT_COLOR)
title_rect = splash_title.get_rect()
inst_rect = instructions.get_rect()

def show_word_list(screen, word_list):
    # print(f'show_word_list: {word_list}')
    screen_rect = screen.get_rect()
    list_length = len(word_list)
    for i in range(list_length):
        word = word_list[i]
        word_image = word_bubble(word)
        screen.blit(word_image, (0, (i*40)))
    screen.blit(instructions, 
                ((screen_rect.centerx-(inst_rect.width/2)), 
                 (screen_rect.height-(inst_rect.height))))

def errorscreen(screen):
    error_rect = error_image.get_rect()
    error_text = 'Try Again'
    error_txt_image = pygame.font.Font(None, 64).render(error_text, True, (0,0,0))
    txt_rect = error_txt_image.get_rect()
    screen_rect = screen.get_rect()
    screen.blit(error_image, ((screen_rect.centerx-error_rect.centerx), (screen_rect.centery-error_rect.centery)))
    error_image.blit(error_txt_image, ((error_rect.centerx-txt_rect.centerx), (error_rect.centery-txt_rect.centery)))
    pygame.display.flip()

def error(screen):
    timer = 50
    while timer > 0:
        errorscreen(screen)
        timer -= 1
    
def word_ready(screen):
    circle_radius = 50
    pygame.draw.circle(screen, (0,255,0),(55, 55), circle_radius)
    pygame.display.flip()

def word_bubble(word):
    word_length = len(word)
    word_text = f'{word_length} {word}'
    word_image = pygame.font.Font(None, 32).render(word_text, True, TEXT_COLOR)
    return  (word_image)

def loadScreen(screen, bg_image):
    screen_rect = screen.get_rect()
    splash_image = pygame.image.load(bg_image)
    splash_image = pygame.transform.scale(splash_image, (1080, 606))
    screen.blit(splash_image, (0,0))
    screen.blit(splash_title, (screen_rect.centerx - (title_rect.width/2), screen_rect.centery))
