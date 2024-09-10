import pygame
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

TITLE_TEXT = 'BananaMan!'
INSTRUCTION_TEXT = 'Press SPACE to begin...'
TITLE_COLOR = (97,97,56)
TEXT_COLOR = (0,0,0)
BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
WORD_COUNT = 5
splash_image = pygame.image.load(BACKGROUND_IMAGE)
splash_image = pygame.transform.scale(splash_image, (1080, 606))

filepath = 'data/words.txt'

chrome_options = Options()
chrome_options.add_argument("--headless")
pygame.init()

# returns TITLE_TEXT as surface
def get_title():
    title = pygame.font.Font(None, 64).render(TITLE_TEXT, True, TITLE_COLOR)
    return title

# returns list of words as array of strings
# get words from website
def get_words_from_web():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.randomlists.com/random-words")
    driver.get_screenshot_as_file("screenshots/driver_screenshot.png") 
    words = driver.find_elements(By.CLASS_NAME, "rand_large")
    word_list = []
    for word in words:
        word = word.text
        word_list.append(word)
    return word_list
    
# get word list from text file
def get_words_from_file(textfile):
    word_list = []
    with open(textfile, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.rstrip('\n')
            if line.isalpha():
                word_list.append(line)
    return word_list
    
# create a word list from large list of words
def get_words():
    word_list = []
    long_list = get_words_from_file(filepath)
    for i in range(WORD_COUNT):
        new_word = select_word(long_list)
        while new_word not in word_list:
            word_list.append(new_word)
    print(f'++> {WORD_COUNT} random words: {word_list}')
    return word_list

# returns a random word from the list of words
def select_word(list):
    length = len(list)
    index = randint(0, length-1)
    return list[index]

# show bubble for each possible word
def show_word_bubbles(screen, wordBubbles):
    screen_rect = screen.get_rect()
    list_length = len(wordBubbles)
    for i in range(list_length):
        bubble = wordBubbles[i]
        bubble.rect.x = (screen_rect.w-300) 
        bubble.rect.y = (i*42)+(screen_rect.h-250)
        bubble.draw(screen)
    # pygame.display.flip()

# returns word as Surface
def word_image(word):
    word_length = len(word)
    word_text = f'{word_length} {word}'
    word_image = pygame.font.Font(None, 32).render(word_text, True, TEXT_COLOR)
    return (word_image)

# returns word list as WordBubbles in an array
def get_bubbles(word_list):
    words = []
    for i in range(len(word_list)):
        word = word_list[i]
        b_word = bubble_word(word, i)
        words.append(b_word)
    return words

# returns word as a WordBubble
def bubble_word(word, index):
    wordImage = word_image(word)
    word_rect = wordImage.get_rect()
    word_bubble = WordBubble(index, word_rect.x, word_rect.y, word_rect.w, word_rect.h, word)
    return word_bubble

# def new_words_button(screen):
def newWords_button(screen):
    screen_rect = screen.get_rect()
    left = screen_rect.centerx-150
    top = screen_rect.h-150
    button_rect = pygame.draw.rect(screen, (0,255,0), (left, top, 300, 100))

class WordBubble:
    def __init__(self, index, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.index = index
        self.color = (200,200,200)
        self.text_color = (0,0,0)
        self.text = text
        self.txt_surface = pygame.font.Font(None, 64).render(self.text, True, self.text_color)
        # self.length_surface = pygame.font.Font(None, 64).render(self.text_length, True, self.text_color)
        # self.length_rect = self.length_surface.get_rect()
        self.index_surface = pygame.font.Font(None, 64).render(f'{self.index+1})', True, self.text_color)
        self.submitted_text = ''
        self.rect.width = self.txt_surface.get_width()
        self.rect.height = self.txt_surface.get_height()
    def update(self):
        # Resize the box if the text is too long.
        width = max(10, self.txt_surface.get_width())
        height = max(10, self.txt_surface.get_height())
        self.rect.w = width
        self.rect.h = height
    def make_bubble_letters(self, screen, text):
        text_length = len(text)
        if text_length > 12:
            difficulty = "long"
            letter_width = 300/text_length
        elif text_length < 6:
            difficulty = "short"
            letter_width = 30
        else:
            difficulty = "medium"
            letter_width = 25
        
        for i in range(len(text)):
            letter_height = 40
            pygame.draw.ellipse(screen, (0,0,25), (self.rect.x+(i*letter_width), self.rect.y, letter_width, letter_height))
    def draw(self, screen):
        self.make_bubble_letters(screen, self.text)
        screen.blit(self.index_surface, (self.rect.x-40, self.rect.y))




