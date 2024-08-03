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

print("BANANAMAN!!!!!!!!!!!!")

pygame.init()
screen = pygame.display.set_mode((1080, 800))
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 64)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, (0, 0, 0), (0, 0, 0))
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text = event.unicode.upper()
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, (0,0,0), (255,255,255))
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
        
    def draw(self, screen):
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x, self.rect.y))

def main():
    clock = pygame.time.Clock()
    input_box1 = InputBox((screen.get_width()/2), (screen.get_height()/2), 280, 64)
    input_boxes = [input_box1]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            for box in input_boxes:
                box.handle_event(event)

            # if event.type == pygame.VIDEORESIZE:
            #     # There's some code to add back window content here.
            #     surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        screen.fill((0, 0, 250))
        
        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pygame.quit()     

print('<<<<<<<<<<<<<<<<<<<< END >>>>>>>>>>>>>>>>>>>>>')
