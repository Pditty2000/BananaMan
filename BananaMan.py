import pygame
import sys
import string
from random import randint
import pregame
import word

pygame.init()
SCREEN_SIZE = (1080, 606)
BACKGROUND_COLOR = (0,0,200)
BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
COLOR_HIDDEN = (0,0,0)
COLOR_SHOWN = (0,255,255)
FONT = pygame.font.Font(None, 64)
smallFONT = pygame.font.Font(None, 32)
FOUND_COUNT = 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen_width = screen.get_width()
screen_height = screen.get_height()

class LetterSpace:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.originx = self.rect.centerx
        self.originy = self.rect.centery
        self.is_shown = False
        self.text = text
        self.color = (0,0,0)
        self.text_color = COLOR_HIDDEN
        self.txt_surface = FONT.render(text, True, self.text_color)
    def sparkle(self):
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        if red < 175 and green < 175 and blue < 175:
            self.text_color = (0,0,0)
        else:
            self.text_color = (255,255,255)
        self.color = (red,green,blue)

    def jiggle(self):
        choice = randint(0, 1)
        x_dist = abs(self.originx-self.rect.centerx)
        y_dist = abs(self.originy-self.rect.centery)
        move_dist = randint(0, 2)
        if choice == 0:
            self.rect.centerx += move_dist
        elif choice == 1:
            self.rect.centery += move_dist
        elif choice == 2:
            self.rect.centerx -= move_dist
        elif choice == 3:
            self.rect.centery -= move_dist
        elif choice == 4:
            self.rect.centerx += move_dist
            self.rect.centery += move_dist
        elif choice == 5:
            self.rect.centerx -= move_dist
            self.rect.centery -= move_dist
        elif choice == 6:
            self.rect.centerx += move_dist
            self.rect.centery -= move_dist
        elif choice == 7:
            self.rect.centerx -= move_dist
            self.rect.centery += move_dist
        if x_dist > 20:
            self.rect.centerx = self.originx
        if y_dist > 20:
            self.rect.centery = self.originy
    def show(self):
        self.is_shown = True
        self.update()
    def hide(self):
        self.is_shown = False
        self.update()
    def update(self):
        if self.is_shown:
            self.color = COLOR_SHOWN
        else:
            self.color = COLOR_HIDDEN
    def draw(self, screen):
        if self.text == ' ':
            self.color = BACKGROUND_COLOR
        pygame.draw.rect(screen, self.color, self.rect)
        centerOffset = (self.rect.w - self.txt_surface.get_width())/2        
        screen.blit(self.txt_surface, (self.rect.x + centerOffset, self.rect.y))

class StatBox:
    def __init__(self, x, y, w, h, length):
        self.count = 0
        self.remaining = length
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

def submitInput(input, letter_spaces):
    count = remaining = 0
    success = False
    letters_length = len(letter_spaces)
    for i in range(letters_length):
        if letter_spaces[i].text == input:
            letter_spaces[i].show()
            success = True
        if letter_spaces[i].is_shown:
            count+=1
        else:
            if letter_spaces[i].text != ' ':
                remaining+=1
    return (count, remaining, success)

def winner_banner(letter_spaces):
    timer = 1000
    bg_banner = 'Images/Winner_banner_1080x675.png'
    bg_image = pygame.image.load(bg_banner)

    while timer > 0:
        timer -=1
        screen.blit(bg_image, (0,0))
        # draw the answer letter boxes
        for letter in letter_spaces:
            letter.jiggle()
            letter.sparkle()
            letter.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                timer = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                timer = 0
            if event.type == pygame.KEYDOWN:
                timer = 0
        pygame.display.flip()

# see if input is letterin phrase
def guess(guess_count, input, letter_spaces):
    done = False
    guess_count.count += 1
    guess = submitInput(input, letter_spaces)
    if not guess[2]:
        pregame.error(screen)
        guess_count.errors+=1
    guess_count.correct = guess[0]
    guess_count.remaining = guess[1]
    if guess_count.remaining <= 0:
        winner_banner(letter_spaces)
        done = True
    return done

# create LetterSpaces for the phrase letters - default hidden
def get_letter_spaces(PHRASE):
    phrase_length = len(PHRASE)
    letter_spaces = []
    for i in range(phrase_length):
        letter_space = LetterSpace(((i*50)+100), 100, 40, 40, PHRASE[i])
        letter_spaces.append(letter_space)
    return letter_spaces

# create buttons for selecting letters - default shown
def get_letter_buttons():
    letter_buttons = []
    alpha_list = list(string.ascii_uppercase)    
    for i in range(13):
        letter_button = LetterSpace(((i*50)+100), 200, 40, 40, alpha_list[i])
        letter_button.show()
        letter_buttons.append(letter_button)
    for i in range(13):
        letter_button = LetterSpace(((i*50)+100), 250, 40, 40, alpha_list[i+13])
        letter_button.show()
        letter_buttons.append(letter_button)
    return letter_buttons

def main(PHRASE):
    clock = pygame.time.Clock()

    # make letter spaces
    PHRASE = PHRASE.upper()
    phrase_length = len(PHRASE)
    letter_spaces = get_letter_spaces(PHRASE)

    # make alphabet buttons  
    letter_buttons = get_letter_buttons()

    # make stat box area
    guess_count = StatBox((screen_width-(screen_width/4)), (screen_height-160), (screen_width/4), 160, phrase_length)

    # start playing
    input1 = ''
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in letter_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.hide()
                        done = guess(guess_count, button.text, letter_spaces)     
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and input1 != '':
                for button in letter_buttons:
                    if button.text == input1:
                        button.hide()
                        done = guess(guess_count, input1, letter_spaces)

        input_letter = FONT.render(input1, True, (0,0,0))
            
            # # if I need to make it resizeable
            # if event.type == pygame.VIDEORESIZE:
            #     # There's some code to add back window content here.
            #     surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)


    # start the displaying   
        # fill background color
        screen.fill(BACKGROUND_COLOR)

        # show input letter (last key typed) and submitted letter
        screen.blit(input_letter, (screen_width/2, screen_height/2))

        # show guess count totals
        guess_count.update()
        guess_count.draw(screen)

        # draw the answer letter boxes
        for letter in letter_spaces:
            letter.draw(screen)
        
        # draw the alphabet
        for button in letter_buttons:
            button.draw(screen)


        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    pygame.display.set_caption("BananaMan!")

    word_list = word.get_words()
    # print(f'===> word_list: {word_list}')

    pygame.display.flip()

    the_count =  0
    running = True
    while running:   
        the_count += 1    
        wordBubbles = word.get_bubbles(word_list)
        word.show_word_bubbles(screen, wordBubbles)
        pregame.loadScreen(screen, BACKGROUND_IMAGE, word_list)
        pregame.show_list(screen, word_list)
        new_list_button = pregame.show_button(screen)
        pygame.display.flip()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if new_list_button.collidepoint(mouse_pos):
                        word_list = word.get_words()
                    for bubble in wordBubbles:
                        if bubble.rect.collidepoint(mouse_pos):
                            print(f'~~~> selected word: {bubble.text}')
                            phrase = bubble.text
                            main(phrase)
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        phrase = word_list[0]
                    elif event.key == pygame.K_2:
                        phrase = word_list[1]
                    elif event.key == pygame.K_3:
                        phrase = word_list[2]
                    elif event.key == pygame.K_4:
                        phrase = word_list[3]
                    elif event.key == pygame.K_5:
                        phrase = word_list[4] 
                    else:
                        phrase = word_list[randint(0, (len(word_list)-1))]
                    print(f'====> main phrase: {phrase}')
                    main(phrase)

print(f'<<<<<<<<<<<<<<<<<<<< END >>>>>>>>>>>>>>>>>>>>>{the_count}')


