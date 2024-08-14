import pygame
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
pygame.init()

TITLE_TEXT = 'BananaMan!'
TITLE_FONT = pygame.font.Font(None, 64)
splash_title = TITLE_FONT.render(TITLE_TEXT, True, (0,0,0))
title_rect = splash_title.get_rect()
INSTRUCTION_TEXT = 'Press SPACE to begin...'
INSTRUCTION_FONT = pygame.font.Font(None, 32)
instructions = INSTRUCTION_FONT.render(INSTRUCTION_TEXT, True, (0,0,0))
inst_rect = instructions.get_rect()


BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
splash_image = pygame.image.load(BACKGROUND_IMAGE)
splash_image = pygame.transform.scale(splash_image, (1080, 606))

chrome_options = Options()
chrome_options.add_argument("--headless")

def get_title_image():
    return TITLE_FONT.render(TITLE_TEXT, True, (0,0,0))

def get_words():
    pygame.display.flip()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.randomlists.com/random-words")
    driver.get_screenshot_as_file("screenshots/driver_screenshot.png") 
    words = driver.find_elements(By.CLASS_NAME, "rand_large")
    word_list = []
    for word in words:
        # print(f'~~~~> word: {word.text}')
        word_list.append(word.text)
    return word_list

def select_word():
    word_list = get_words()
    list_length = len(word_list)
    word_index = randint(0, list_length)
    print(f'list length: {list_length}, index: {word_index}')
    word = word_list[word_index]
    return word

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

def word_bubble(word):
    word_length = len(word)
    word_text = f'{word_length} {word}'
    word_image = pygame.font.Font(None, 32).render(word_text, True, (0,0,0))
    return  (word_image)
