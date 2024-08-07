import pygame
import random

pygame.init()
BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
BACKGROUND_COLOR = (0,255,0)
TEXT_COLOR = (255, 255, 255)

splash_image = pygame.image.load(BACKGROUND_IMAGE)

def splashscreen(screen):
    print(f'Got to splashscreen: {screen}')
    # screen.fill((BACKGROUND_COLOR))
    screen.blit(splash_image, (0, 0))


    print(f' after blit splash image')
    

