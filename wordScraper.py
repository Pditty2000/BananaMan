import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome()
driver.get("https://www.vocabulary.com/lists/52473")
driver.get_screenshot_as_file("screenshots/driver_screenshot.png") 
words = driver.find_elements(By.CLASS_NAME, "count")
words_length = len(words)
print(f'words length: {words_length}')
# for i in range(words_length):
#     word = words[i]
#     test = word.get_attribute('html')
#     print(f'_____> test: {test}')


# <a class="word" href="/dictionary/consider" title="deem to be"><span class="count"></span> consider</a>
