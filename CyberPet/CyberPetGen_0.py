import pygame
import sys, os

WIDTH, HEIGHT = 480, 360
FPS = 60

#        R   G   B
GREY  = (80 ,80 ,80 )
BLACK = (0,  0,  0  )
WHITE = (255,255,255)


class Action(object):
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def do(self):
        return self.func(*self.args)

def main():
    global DISPLAY, CLOCK, update_sequence

    pygame.init()

    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    update_sequence = [()]
    eye1rect = pygame.Rect((185, 110, 25, 100))
    eye2rect = pygame.Rect((265, 110, 25, 100))
    pygame.display.set_caption("CyberPet Gen.0")
    pygame.display.set_icon(image('icon.png'))
    while True:  # Game Loop
        DISPLAY.fill(GREY)
        face_rect = draw_face(DISPLAY)
        draw_eyes(DISPLAY, eye1rect, eye2rect, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        CLOCK.tick(FPS)


def image(path):
    return pygame.image.load(path).convert_alpha()


def draw_face(surface):
    face_rect = pygame.Rect(0, 0, HEIGHT / 2, HEIGHT / 2)
    face_rect.center = (WIDTH / 2, HEIGHT / 2)
    pygame.draw.rect(surface, WHITE, face_rect)
    pygame.draw.rect(surface, BLACK, face_rect, 5)
    return face_rect


def draw_eyes(surface, eye1rect, eye2rect, color):
    pygame.draw.rect(surface, color, eye1rect)
    pygame.draw.rect(surface, BLACK, eye1rect, 5)
    pygame.draw.rect(surface, color, eye2rect)
    pygame.draw.rect(surface, BLACK, eye2rect, 5)
    return eye1rect, eye2rect


def add_action(action, frame):
    try:
        update_sequence[frame].append(action)
    except IndexError:
        frame.append((action,))


def do_next(surface):
    action_sequence = update_sequence[0]
    for action in action_sequence:
        action.do()
    update_sequence.pop(0)


def blink(eye1rect, eye2rect, speed):
    center1, center2 = eye1rect.center, eye2rect.center
    eye1rect_new, eye2rect_new = eye1rect.copy(), eye2rect.copy()
    for i in range(0, 240, speed):
        add_action(Action(draw_eyes), eye1rect_new)
        # TODO Okay I'm gonna sleep now check this website for formula tomorrow:
        # https://www.wolframalpha.com/input/?i=y%3D√%7C100x%7C


if __name__ == '__main__':
    main()
