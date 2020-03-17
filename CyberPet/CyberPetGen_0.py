import pygame
import sys, os
import math
import random

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

    def __repr__(self):
        return self.func.__name__ + str(self.args)


def main():
    global DISPLAY, CLOCK, update_sequence, status

    pygame.init()

    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    update_sequence = [[]]
    status = {'blinking': False}

    eye1rect = pygame.Rect((185, 110, 25, 100))
    eye2rect = pygame.Rect((265, 110, 25, 100))
    pygame.display.set_caption("CyberPet Gen.0")
    pygame.display.set_icon(image('icon.png'))
    while True:  # Game Loop
        # if update_sequence: print(update_sequence)
        DISPLAY.fill(GREY)
        face_rect = draw_face(DISPLAY)
        do_next()
        if not status['blinking']:
            draw_eyes(DISPLAY, eye1rect, eye2rect, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if random.randint(0,1) == 0:
                    blink_twice(DISPLAY, eye1rect, eye2rect, 8)
                else:
                    blink(DISPLAY, eye1rect, eye2rect, 8)
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


def add_action(action, frame:int):
    try:
        update_sequence[frame].append(action)
    except IndexError:
        update_sequence.append([action])


def do_next():
    try:
        action_sequence = update_sequence[0]
        for action in action_sequence:
            action.do()
        update_sequence.pop(0)
    except IndexError:
        return


def blink(surface, eye1rect, eye2rect, speed, offset=0):
    center1, center2 = eye1rect.center, eye2rect.center
    eye1rect_new, eye2rect_new = eye1rect.copy(), eye2rect.copy()
    init_w1, init_h1 = eye1rect_new.size
    init_w2, init_h2 = eye2rect_new.size
    add_action(Action(modify_status, 'blinking', True), offset)
    for i in range(0, int(240/speed)):
        height_multiplier = math.sqrt(abs((i/120*speed)-1))  # y = √|x-1|, x∈[0,2]
        width_multiplier = -0.125*i/120 * (i/60-4) + 1  # y = -0.0625x(x-4)+1, x∈[0,4]
        add_action(Action(draw_eyes, surface, eye1rect_new, eye2rect_new, BLACK), i+offset)
        # Shapeshift the eyes
        eye1rect_new, eye2rect_new = eye1rect_new.copy(), eye2rect_new.copy()
        eye1rect_new.height, eye2rect_new.height = \
            init_h1*height_multiplier, init_h2*height_multiplier
        eye1rect_new.width, eye2rect_new.width = \
            init_w1*width_multiplier, init_w2*width_multiplier
        eye1rect_new.center, eye2rect_new.center = center1, center2
        print(eye1rect_new.height, eye2rect_new.height)
    add_action(Action(modify_status, 'blinking', False), int(240/speed)+offset)


def blink_twice(surface, eye1rect, eye2rect, speed):
    blink(surface, eye1rect, eye2rect, speed)
    blink(surface, eye1rect, eye2rect, speed, offset=int(240/speed)+random.randint(1,30))
    print('blink twice added')
    print(update_sequence)


def modify_status(key, value):
    status[key] = value
    return key, value


if __name__ == '__main__':
    main()
