import pygame
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
pygame.init()

def get_words():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://random-word-generator.net/")
    driver.get_screenshot_as_file("screenshots/driver_screenshot.png") 
    words = driver.find_elements(By.CLASS_NAME, "random_word")
    word_list = []
    for word in words:
        print(f'~~~~> word: {word.text}')
        word_list.appent(word.text)
    return word_list

def select_word():
    word_list = get_words()
    word_index = randint(0, 4)
    word = word_list[word_index]
    return word

