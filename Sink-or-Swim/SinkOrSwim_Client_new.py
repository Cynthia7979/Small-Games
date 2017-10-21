import socket, pygame
from pygame.locals import *

#         R    G    B
WHITE = (255, 255 ,255)

# image files and their rect

def main():
    window_width = 700
    window_height = 300
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((window_width,window_height))
    FPS = 30
    CLOCK = pygame.time.Clock()
    screen = 'join'
    while True:
        DISPLAYSURF.fill(WHITE)
        if screen == 'join':
            loadImage('./sink_or_swim_logo.png',DISPLAYSURF,(0,0))
        pygame.display.update()
        CLOCK.tick(FPS)


def loadImage(path, surf, pos,func=None):
    image = pygame.image.load(path)
    imageRect = image.get_rect()
    imageRect.topleft = pos
    surf.blit(image,imageRect)
    return image, imageRect


main()