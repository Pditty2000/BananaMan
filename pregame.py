import pygame
import random
import word

pygame.init()
# BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
ERROR_IMAGE = 'Images/error.png'
BACKGROUND_COLOR = (255,255,255)
error_image = pygame.image.load(ERROR_IMAGE)
error_image = pygame.transform.scale(error_image, (606, 606))

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
    
def loadScreen(screen, bg_image):
    screen_rect = screen.get_rect()
    splash_image = pygame.image.load(bg_image)
    splash_image = pygame.transform.scale(splash_image, (1080, 606))
    splash_title = word.get_title_image()
    title_rect = splash_title.get_rect()    
    screen.blit(splash_image, (0,0))
    screen.blit(splash_title, (screen_rect.centerx - (title_rect.width/2), screen_rect.centery))
