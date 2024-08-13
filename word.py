import pygame
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
splash_image = pygame.image.load(BACKGROUND_IMAGE)
splash_image = pygame.transform.scale(splash_image, (1080, 606))

chrome_options = Options()
chrome_options.add_argument("--headless")
pygame.init()

def get_words(screen):
    screen.blit(splash_image, (0,0))
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

