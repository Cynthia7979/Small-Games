import socket, pygame
#         R    G    B
WHITE = (255, 255 ,255)
def main():
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    while True:
        DISPLAYSURF.fill(WHITE)

main()