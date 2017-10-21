# This is a test input box
import pygame, sys
from pygame.locals import *

def main():
    WIDTH = 400
    HEIGHT = 300
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.Font('arial.ttf', 32)
    inputingWord = False
    inputBox = pygame.Rect(50,250,300,35)
    currentWords = []
    while True:
        DISPLAYSURF.fill(WHITE)
        pygame.draw.rect(DISPLAYSURF,BLACK,inputBox)
        displayWord = ''.join(currentWords)
        wordSurf = FONT.render(displayWord,True,WHITE)
        wordRect = wordSurf.get_rect()
        wordRect.topleft = (50,250)
        DISPLAYSURF.blit(wordSurf,wordRect)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                x,y = event.pos
                posRect = pygame.Rect(x,y,1,1)
                if posRect.colliderect(inputBox):
                    inputingWord = True
                else:
                    inputingWord = False
            elif event.type == KEYUP:
                if inputingWord:
                    key = event.key
                    if key == K_RETURN:
                        inputingWord = False
                        break
                    elif key == K_BACKSPACE:
                        if len(currentWords) >= 1:
                            del currentWords[-1]
                    else:
                        print chr(key)
                        currentWords.append(chr(key))
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        CLOCK.tick(30)
        pygame.display.flip()

main()