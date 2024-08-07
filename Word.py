import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
pygame.init()


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://random-word-generator.net/")
driver.get_screenshot_as_file("screenshots/driver_screenshot.png") 
words = driver.find_elements(By.CLASS_NAME, "random_word")
for word in words:
    print(f'~~~~> word: {word.text}')
print()
print('--- Done ---')