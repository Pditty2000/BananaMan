# Front end:
# make screen/background
# make letter selection grid
#    make letter selected
#    make letter used warning
# make text input box
# make submit button
# make gallows
# make character
# make hidden letter display
#    make found letter display
# make success banner
# Back end:
# collect input from text box on submit or
# collect input from letter grid on mouseclick
#      verify if used already
#           if not, make letter selected
#           if so, send warning

import pygame
import sys
from random import randint
import landingPage
import word

pygame.init()
BACKGROUND_COLOR = (0,0,200)
COLOR_UNFOUND = (0,0,0)
COLOR_FOUND = (0,255,255)
FONT = pygame.font.Font(None, 64)
smallFONT = pygame.font.Font(None, 32)
FOUND_COUNT = 0


# class InputBox:
#     def __init__(self, x, y, w, h, text=''):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.color = (200,200,200)
#         self.text_color = (0,0,0)
#         self.text = text
#         self.txt_surface = FONT.render(self.text, True, self.text_color)
#         self.submitted_text = ''
#         # Re-render the text.
#         self.txt_surface = FONT.render(self.text, True, self.text_color)
#     def update(self):
#         # Resize the box if the text is too long.
#         width = max(10, self.txt_surface.get_width())
#         height = max(10, self.txt_surface.get_height())
#         self.rect.w = width
#         self.rect.h = height
#     def draw(self, screen):
#         # pygame.draw.rect(screen, self.color, self.rect)
#         screen.blit(self.txt_surface, (self.rect.x, self.rect.y))

class LetterSpace:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.isfound = False
        self.text = text
        self.color = (0,0,0)
        self.text_color = COLOR_UNFOUND
        self.txt_surface = FONT.render(text, True, self.text_color)
    def found(self):
        self.isfound = True
        self.update()
    def update(self):
        if self.isfound:
            self.color = COLOR_FOUND
    def draw(self, screen):
        if self.text == ' ':
            self.color = BACKGROUND_COLOR
        pygame.draw.rect(screen, self.color, self.rect)
        centerOffset = (self.rect.w - self.txt_surface.get_width())/2        
        screen.blit(self.txt_surface, (self.rect.x + centerOffset, self.rect.y))

class StatBox:
    def __init__(self, x, y, w, h):
        self.count = 0
        self.remaining = 0
        self.correct = 0
        self.errors = 0
        self.color = (150,150,150)
        self.rect = pygame.Rect(x, y, w, h)
        self.text_color = (0,0,0)
    def update(self):
        self.count_text = smallFONT.render(f'Total Guesses: {self.count}', True, self.text_color)
        self.correct_text = smallFONT.render(f'{self.correct} correct', True, self.text_color)
        self.error_text = smallFONT.render(f'{self.errors} errors', True, self.text_color)
        self.remain_text = smallFONT.render(f'{self.remaining} remaining', True, self.text_color)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.count_text, (self.rect.x+10, (screen_height-self.rect.h+5)))
        screen.blit(self.correct_text, (self.rect.x+10, self.rect.y+(self.rect.h/4)))
        screen.blit(self.error_text, (self.rect.x+10, self.rect.y+(2*(self.rect.h/4))))
        screen.blit(self.remain_text, (self.rect.x+10, self.rect.y+(3*(self.rect.h/4))))

def submitInput(input, phrase_length, letter_spaces):
    count = remaining = 0
    success = False
    for i in range(phrase_length):
        if letter_spaces[i].text == input:
            letter_spaces[i].found()
            success = True
        if letter_spaces[i].isfound:
            count+=1
        else:
            if letter_spaces[i].text != ' ':
                remaining+=1
    return (count, remaining, success)

def main(PHRASE):
    clock = pygame.time.Clock()

    # make phrase
    # PHRASE = "This is a TEST"
    PHRASE = PHRASE.upper()

    # make letter spaces
    letter_spaces = []
    phrase_length = len(PHRASE)
    for i in range(phrase_length):
        letter_space = LetterSpace(((i*50)+100), 100, 40, 40, PHRASE[i])
        letter_spaces.append(letter_space)

    # make count area
    guess_count = StatBox((screen_width-(screen_width/4)), (screen_height-160), (screen_width/4), 160)


    # start playing
    input1 = ''
    submitted_input = ''
    error_count = 0
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
            if event.type == pygame.KEYDOWN:
                e_key = event.key
                if e_key in range(pygame.K_a, pygame.K_z + 1):
                    input1 = event.unicode.upper()
                if e_key == pygame.K_RETURN and input1 != '':
                    guess_count.count += 1
                    guess = submitInput(input1, phrase_length, letter_spaces)
                    submitted_input = input1
                    print(f'count: {guess[0]}, remaining: {guess[1]}')
                    if not guess[2]:
                        landingPage.error(screen)
                        error_count+=1
                    guess_count.correct = guess[0]
                    guess_count.remaining = guess[1]
                    guess_count.errors = error_count
                    input1 = ''

        input_letter = FONT.render(input1, True, (0,0,0))
        submitted_letter = FONT.render(submitted_input, True, ((255,0,0)))
            
            # # if I need to make it resizeable
            # if event.type == pygame.VIDEORESIZE:
            #     # There's some code to add back window content here.
            #     surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


    # start the displaying   
        # fill background color
        screen.fill(BACKGROUND_COLOR)

        # show input letter (last key typed) and submitted letter
        screen.blit(input_letter, (screen_width/2, screen_height/2))
        screen.blit(submitted_letter, (screen_width/2, screen_height/2-40))

        # show guess count totals
        guess_count.update()
        guess_count.draw(screen)

        # draw the answer letter boxes
        for letter in letter_spaces:
            letter.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    pygame.display.set_caption("BananaMan!")

    # pygame setup
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1080, 606))
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    BACKGROUND_COLOR = (0,0,200)
    COLOR_UNFOUND = (0,0,0)
    COLOR_FOUND = (0,255,255)
    FONT = pygame.font.Font(None, 64)
    smallFONT = pygame.font.Font(None, 32)
    word_list = word.get_words()
    the_count =  0
    
    phrase = "TEST"

    running = True
    while running:   
        the_count += 1     
        # show landing page before starting game
        landingPage.splashscreen(screen, word_list)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print(f'====> main phrase: {phrase}')
                        main(phrase)
                    # elif event.key == pygame.K_t:
                    #     word.get_words()
                    else:
                        landingPage.error(screen)

print(f'<<<<<<<<<<<<<<<<<<<< END >>>>>>>>>>>>>>>>>>>>>{the_count}')
