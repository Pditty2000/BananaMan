import pygame
import json
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


pygame.init()
FONT = pygame.font.Font(None, 64)
screen = pygame.display.set_mode((800, 600))
screen.fill((255,255,255))

ff_options = Options()
ff_options.add_argument("--headless")

def get_definition(the_word):
    definitions = []
    driver = webdriver.Chrome()
    driver.get(f'https://www.yourdictionary.com/{the_word}')
    print('page opened')
    definition = driver.find_element(By.CLASS_NAME, 'inline-block text-black text-base sm:text-lg sm:leading-6 mb-1')
    print(f'+++++> definition: {definition}')
    
    return definition

word_list = []
f = open('data/word_list.json')
json_list = json.load(f)
for i in json_list:
    word_list.append(i)
list_length = len(word_list)
index = randint(0, list_length)

done = False
limit = list_length
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
    if limit <= 0:
        done = True
    print(f'running: {limit}')

    screen.fill((255,255,255))
    # the_word = word_list[limit-1]
    the_word = 'Test'
    limit_text = FONT.render(f'limit: {limit}', True, (255,0,0))
    word_text = FONT.render(f'random word: {the_word}', True, (0,0,0))

    # print(f'word_list length: {len(word_list)}, word_list[{index}]: {word_list[index]}')
    screen.blit(limit_text, (screen.get_width()/2, screen.get_height()/2))
    screen.blit(word_text, (0, ((screen.get_height()/2)+50)))
    limit -= 1
    pygame.display.flip()
    definitions = get_definition(the_word)



