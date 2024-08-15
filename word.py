import pygame
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

TITLE_TEXT = 'BananaMan!'
INSTRUCTION_TEXT = 'Press SPACE to begin...'
TEXT_COLOR = (0,0,0)
BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
splash_image = pygame.image.load(BACKGROUND_IMAGE)
splash_image = pygame.transform.scale(splash_image, (1080, 606))

chrome_options = Options()
chrome_options.add_argument("--headless")
pygame.init()

# returns list of words as array of strings
def get_words():
    pygame.display.flip()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.randomlists.com/random-words")
    driver.get_screenshot_as_file("screenshots/driver_screenshot.png") 
    words = driver.find_elements(By.CLASS_NAME, "rand_large")
    word_list = []
    for word in words:
        word = word.text
        word_list.append(word)
    return word_list

def show_word_bubbles(screen, wordBubbles):
    screen_rect = screen.get_rect()
    list_length = len(wordBubbles)
    test_rect = pygame.Rect(screen_rect.centerx-100, screen_rect.centery-250, 200, 100)
    print(f'======> show bubbles..')
    pygame.draw.ellipse(screen, (0,0,255), test_rect)
    for i in range(list_length):
        bubble = wordBubbles[i]
        bubble.rect.x = screen_rect.w-bubble.rect.w-10
        bubble.rect.y = (i*(bubble.rect.h))+5
        print(f'==> bubble.rect: {bubble.rect}')
        bubble.draw(screen)


# display word list on splash page
def show_word_list(screen, word_list):
    instructions = pygame.font.Font(None, 32).render(INSTRUCTION_TEXT, True, TEXT_COLOR)
    inst_rect = instructions.get_rect()
    screen_rect = screen.get_rect()
    list_length = len(word_list)
    for i in range(list_length):
        word = word_list[i]
        wordImage = word_image(word)
        screen.blit(wordImage, (0, (i*40)))
    screen.blit(instructions, 
                ((screen_rect.centerx-(inst_rect.width/2)), 
                 (screen_rect.height-(inst_rect.height))))

# returns word as Surface
def word_image(word):
    word_length = len(word)
    word_text = f'{word_length} {word}'
    word_image = pygame.font.Font(None, 32).render(word_text, True, TEXT_COLOR)
    return  (word_image)

# returns TITLE_TEXT as surface
def get_title():
    title = pygame.font.Font(None, 64).render(TITLE_TEXT, True, TEXT_COLOR)
    return title

# returns word list as WordBubbles in an array
def get_bubbles(word_list):
    words = []
    for word in word_list:
        words.append(bubble_word(word))
    return words

# returns word as a WordBubble
def bubble_word(word):
    wordImage = word_image(word)
    word_rect = wordImage.get_rect()
    word_bubble = WordBubble(word_rect.x, word_rect.y, word_rect.w, word_rect.h)
    return word_bubble

    

class WordBubble:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200,200,200)
        self.text_color = (0,0,0)
        self.text = text
        self.txt_surface = pygame.font.Font(None, 64).render(self.text, True, self.text_color)
        self.submitted_text = ''
        # Re-render the text.
        self.txt_surface = pygame.font.Font(None, 64).render(self.text, True, self.text_color)
    def update(self):
        # Resize the box if the text is too long.
        width = max(10, self.txt_surface.get_width())
        height = max(10, self.txt_surface.get_height())
        self.rect.w = width
        self.rect.h = height
    def draw(self, screen):
        # pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x, self.rect.y))



