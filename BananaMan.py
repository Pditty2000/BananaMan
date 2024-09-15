import pygame
import sys
import string
from random import randint
import pregame
import word

pygame.init()
SCREEN_SIZE = (1080, 606)
BACKGROUND_COLOR = (198,208,149)
BACKGROUND_IMAGE = 'Images/Banana_yellow_background_474x266.png'
G_O_BACKGROUND = 'Images/gameover.jpg'
USED_IMAGE = 'Images/used_clear.png'
COLOR_HIDDEN = (0,0,0)
COLOR_SHOWN = (0,255,255)
FONT = pygame.font.Font(None, 64)
smallFONT = pygame.font.Font(None, 32)
FOUND_COUNT = 0
INPUT_COLOR = (255,75,75)

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
    def reset(self):
        self.rect.centerx = self.originx
        self.rect.centery =  self.originy
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
        self.limit = 100
        self.color = (150,150,150)
        self.rect = pygame.Rect(x, y, w, h)
        self.text_color = (0,0,0)
    def update(self):
        self.count_text = smallFONT.render(f'Guesses Remaining: {self.limit - self.errors}', True, self.text_color)
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

def game_over(letter_spaces):
    timer = 1000
    bg_image = pygame.image.load(G_O_BACKGROUND)
    bg_image = pygame.transform.scale(bg_image, SCREEN_SIZE)
    while timer >= 0:
        timer -= 1
        screen.blit(bg_image, (0, 0))
        for letter in letter_spaces:
            letter.show()
            letter.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                timer = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                timer = 0
            if event.type == pygame.KEYDOWN:
                timer = 0
        pygame.display.flip()

def usedscreen(screen):
    used_image = pygame.image.load(USED_IMAGE)
    used_image = pygame.transform.scale(used_image, (303, 303))
    used_rect = used_image.get_rect()
    used_rect.center = (screen_width/2, screen_height/2)
    screen.blit(used_image, used_rect)
    pygame.display.flip()

def used(screen):
    timer = 100
    while timer > 0:
        usedscreen(screen)
        timer -= 1

# see if input is letter in phrase
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
    if guess_count.limit <= guess_count.errors:
        game_over(letter_spaces)
        print(f'GAME OVER!')
        done = True
    return done

# create LetterSpaces for the phrase letters - default hidden
def get_letter_spaces(PHRASE):
    phrase_length = len(PHRASE)
    letter_spaces = []
    for i in range(phrase_length):
        letter_space = LetterSpace(100, 100, 40, 40, PHRASE[i])
        letter_spaces.append(letter_space)
    center_letter_spaces(letter_spaces)
    return letter_spaces

def center_letter_spaces(letter_spaces):
    box_width = letter_spaces[0].rect.w + 10
    box_height = letter_spaces[0].rect.h + 10
    center = screen_width/2
    spaces = int(screen_width/box_width)
    letters = len(letter_spaces)
    extra_spaces = spaces - letters
    if extra_spaces <= 0: # split into 2 lines if too long for screen
        half = int(letters/2)
        first_slice = letter_spaces[:half]
        second_slice = letter_spaces[half:]
        center_letter_spaces(first_slice)
        for l_space in second_slice:
            l_space.originy += box_height
            l_space.reset()
        center_letter_spaces(second_slice)
    else:
        mid = int(letters/2)
        if letters%2 != 0:
            for i in range(letters):
                letter_space = letter_spaces[i]
                letter_space.originx = center+((i - mid)*box_width)
                letter_space.reset()
        else:
            for i in range(letters):
                letter_space = letter_spaces[i]
                letter_space.originx = center+((i - mid)*box_width)+(box_width/2)
                letter_space.reset()
    return letter_spaces
    
# create buttons for selecting letters - default shown
def get_letter_buttons():
    letter_buttons = []
    alpha_list = list(string.ascii_uppercase)    
    for i in range(26):
        letter_button = LetterSpace(100, 275, 40, 40, alpha_list[i])
        letter_button.show()
        letter_buttons.append(letter_button)

    letter_buttons = center_letter_spaces(letter_buttons)
    return letter_buttons

def get_diff_buttons():
    diff_buttons = []
    midx = screen_width/2
    difficulties = ['1) EASY', '2) MEDIUM', '3) HARD']
    for i in range(len(difficulties)):
        button = LetterSpace(midx-150, 175, 300, 75, difficulties[i])
        diff_buttons.append(button)
    diff_buttons = center_letter_spaces(diff_buttons)
    return diff_buttons

def get_difficulty():
    difficulty = 0
    text = 'Select Difficulty'
    text_surface = pygame.font.Font(None, 64).render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.centerx = screen_width/2
    text_rect.y = 100
    diff_buttons = get_diff_buttons()
    while difficulty == 0:
        mouse_pos = pygame.mouse.get_pos()
        for button in diff_buttons:
            if button.rect.collidepoint(mouse_pos):
                if button.color != COLOR_HIDDEN:
                    button.color = (0,0,255)
            else:
                if button.color != COLOR_HIDDEN:
                    button.color = COLOR_SHOWN
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in diff_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        difficulty = button.text
            if event.type == pygame.QUIT:
                difficulty = -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                difficulty = -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = '1) EASY'
                elif event.key == pygame.K_2:
                    difficulty = '2) MEDIUM'
                elif event.key == pygame.K_3:
                    difficulty = '3) HARD'
                else:
                    print(f'Try Again!')
        screen.fill((190,190,190))
        screen.blit(text_surface, text_rect)
        for button in diff_buttons:
            button.show()
            button.draw(screen)
        pygame.display.flip()
    return difficulty

def main(PHRASE):
    clock = pygame.time.Clock()

    # get user selected difficulty
    difficulty = get_difficulty()
    print(f'++> difficulty: {difficulty}')

    # make letter spaces
    PHRASE = PHRASE.upper()
    # phrase_surface = pygame.font.Font(None, 64).render(PHRASE, True, (0,0,0))
    phrase_length = len(PHRASE)
    letter_spaces = get_letter_spaces(PHRASE)

    # make alphabet buttons  
    letter_buttons = get_letter_buttons()

    # make stat box area
    guess_count = StatBox((screen_width-(screen_width/4)), (screen_height-160), (screen_width/4), 160, phrase_length)
    if difficulty == '3) HARD':
        guess_count.limit = 3
    elif difficulty == '2) MEDIUM':
        guess_count.limit = 5
    elif difficulty == '1) EASY':
        guess_count.limit = 10

    # start playing
    used_letters = []
    input1 = ''
    done = False
    while not done:
        if difficulty == -1:
            done = True
        mouse_pos = pygame.mouse.get_pos()
        for button in letter_buttons:
            if button.rect.collidepoint(mouse_pos):
                if button.color != COLOR_HIDDEN:
                    input1 = button.text
                    button.color = (0,0,255)
            else:
                if button.color != COLOR_HIDDEN:
                    button.color = COLOR_SHOWN
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
                    if input1 in used_letters:
                        used(screen)
                    else:
                        for button in letter_buttons:
                            if button.text == input1:
                                button.hide()
                                used_letters.append(input1)
                                done = guess(guess_count, input1, letter_spaces)
                                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in letter_buttons:
                    if button.rect.collidepoint(mouse_pos) and input1 not in used_letters:
                        button.hide()
                        used_letters.append(input1)
                        done = guess(guess_count, input1, letter_spaces)
                        break    
        input_letter = FONT.render(input1, True, INPUT_COLOR)

    # start the displaying if not done
        if not done:
        # fill background color
            screen.fill(BACKGROUND_COLOR)
        # show input letter (last key typed) and submitted letter
            screen.blit(input_letter, (screen_width/2, 207))
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
    # pygame.display.flip()
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


