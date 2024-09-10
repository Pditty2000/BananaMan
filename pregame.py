import pygame
import word
import random

pygame.init()
# BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
ERROR_IMAGE = 'Images/error.png'
BACKGROUND_COLOR = (0,255,0)
TEXT_COLOR = (0,0,0)
TITLE_FONT = pygame.font.Font(None, 64)

# splash_image = pygame.image.load(BACKGROUND_IMAGE)
# splash_image = pygame.transform.scale(splash_image, (1080, 606))

error_image = pygame.image.load(ERROR_IMAGE)
error_image = pygame.transform.scale(error_image, (606, 606))
# splash_title = TITLE_FONT.render(TITLE_TEXT, True, TEXT_COLOR)
# title_rect = splash_title.get_rect()


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

def loadScreen(screen, bg_image, word_list):
    screen_rect = screen.get_rect()
    splash_image = pygame.image.load(bg_image)
    splash_image = pygame.transform.scale(splash_image, (1080, 606))
    splash_title = word.get_title()
    title_rect = splash_title.get_rect()
    screen.blit(splash_image, (0,0))
    screen.blit(splash_title, (screen_rect.centerx - (title_rect.width/2), 150))

def show_list(screen, word_list):
    wordBubbles = word.get_bubbles(word_list)
    print(f'word_list: {word_list}')
    word.show_word_bubbles(screen, wordBubbles)
    # pygame.display.flip()

def show_button(screen):
    button = get_list_button(screen)
    button_color = (44,242,136)
    pygame.draw.rect(screen, button_color, button)
    return button

def get_list_button(screen):
    button_width = 175
    button_height = 50
    screen_rect = screen.get_rect()
    button_rect = pygame.rect.Rect(screen_rect.centerx-100, screen_rect.centery+50, button_width, button_height)
    return button_rect