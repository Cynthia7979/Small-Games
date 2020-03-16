import pygame
import sys, os

WIDTH, HEIGHT = 480, 360
FPS = 60

#        R   G   B
GREY  = (80 ,80 ,80 )
WHITE = (0,  0,  0  )
BLACK = (255,255,255)


def main():
    global DISPLAY, CLOCK
    pygame.init()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("CyberPet Gen.0")
    pygame.display.set_icon(image('icon.png'))
    while True:  # Game Loop
        DISPLAY.fill(GREY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        CLOCK.tick(FPS)


def image(path):
    return pygame.image.load(path).convert_alpha()


if __name__ == '__main__':
    main()
