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



class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200,200,200)
        self.text_color = (0,0,0)
        self.text = text
        self.txt_surface = FONT.render(self.text, True, self.text_color)
        self.submitted_text = ''
    def handle_event(self, event):
        if event.key == pygame.K_RETURN:
            self.submitted_text = self.text
            self.text = ''
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            e_key = event.key
            if e_key in range(pygame.K_a, pygame.K_z + 1):
                self.text = event.unicode.upper()
        # Re-render the text.
        self.txt_surface = FONT.render(self.text, True, self.text_color)
    def update(self):
        # Resize the box if the text is too long.
        width = max(10, self.txt_surface.get_width())
        height = max(10, self.txt_surface.get_height())
        self.rect.w = width
        self.rect.h = height
    def draw(self, screen):
        # pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x, self.rect.y))

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
        print(f'in found self.isfound: {self.isfound}')
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

class GuessCount:
    def __init__(self, x, y, w, h):
        self.count = 0
        self.wrong = 0
        self.right = 0
        self.color = (150,150,150)
        self.rect = pygame.Rect(x, y, w, h)
        self.text_color = (0,0,0)
        self.count_text = smallFONT.render(f'Total Guesses: {self.count}', True, self.text_color)
        self.wrong_text = smallFONT.render(f'Incorrect: {self.wrong}', True, self.text_color)
        self.right_text = smallFONT.render(f'Correct: {self.right}', True, self.text_color)
    def guess(self):
        self.count += 1
        print(f'guess: self.count: {self.count}')

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.count_text, (self.rect.x+10, (screen_height-self.rect.h+5)))
        screen.blit(self.wrong_text, (self.rect.x+10, self.rect.y+(self.rect.h/3)))
        screen.blit(self.right_text, (self.rect.x+10, self.rect.y+(2*(self.rect.h/3))))


def main():
    input_box1 = InputBox((screen.get_width()/2), (screen.get_height()/2), 1, 1)

    # make phrase
    PHRASE = "This is a TEST"
    PHRASE = PHRASE.upper()

    # make letter spaces
    letter_spaces = []
    phrase_length = len(PHRASE)
    for i in range(phrase_length):
        letter_space = LetterSpace(((i*50)+100), 100, 40, 40, PHRASE[i])
        letter_spaces.append(letter_space)

    # make count area
    guess_count = GuessCount((screen_width-(screen_width/4)), (screen_height-160), (screen_width/4), 160)


    # start playing
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
                    print('it is a letter')
                    input1 = event.unicode.upper()
                    print(f'input1 = {input1}')
                print(f'event: {event.unicode.upper()}')
                input_box1.draw(screen)

                if input_box1.submitted_text != '':
                    guess_count.guess()
                    for i in range(phrase_length):
                        if letter_spaces[i].text == input_box1.submitted_text:
                            letter_spaces[i].found()

            # if event.type == pygame.VIDEORESIZE:
            #     # There's some code to add back window content here.
            #     surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        screen.fill(BACKGROUND_COLOR)
        guess_count.draw(screen)

        input_box1.update()
        input_box1.draw(screen)
        for letter in letter_spaces:
            letter.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        print(f'Clock: {clock}')


if __name__ == '__main__':
    pygame.display.set_caption("BananaMan!")

    # pygame setup
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1080, 800))
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    BACKGROUND_COLOR = (0,0,200)
    COLOR_UNFOUND = (0,0,0)
    COLOR_FOUND = (0,255,255)
    FONT = pygame.font.Font(None, 64)
    smallFONT = pygame.font.Font(None, 32)
    
    testcount =  0
    
    running = True
    while running:
        # built in self destruct button
        if testcount > 10000:
            print( f'Hit the loop limit: testcount = {testcount}')
            running = False
        testcount+=1
        
        # show landing page before starting game
        landingPage.splashscreen(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            else:
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                    main()  

print('<<<<<<<<<<<<<<<<<<<< END >>>>>>>>>>>>>>>>>>>>>')
