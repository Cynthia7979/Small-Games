import pygame
import sys, os
import math
import random
import time
import tkinter as tk
import logging
import chat_module
from ctypes import windll, Structure, c_long, byref  # Keep on top

WIDTH, HEIGHT = 480, 360
FPS = 60

#        R   G   B
GREY  = (80 ,80 ,80 )
BLACK = (0,  0,  0  )
WHITE = (255,255,255)


class Action(object):
    def __init__(self, func, *args, priority=0):
        assert callable(func), 'Received non-function variable:'+str(func)
        self.func = func
        self.args = args
        self.priority = priority

    def do(self):
        try:
            _ = self.func(*self.args)
            LOGGER.debug(f'Called {self.func.__name__}({self.args}).')
            return _
        except Exception as e:
            print(self)
            raise e

    def __repr__(self):
        return self.func.__name__ + str(self.args)

    def __gt__(self, other):
        return self.priority > other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __eq__(self, other):
        return self.priority == other.priority


class RECT(Structure):
    _fields_ = [
    ('left',    c_long),
    ('top',     c_long),
    ('right',   c_long),
    ('bottom',  c_long),
    ]
    def width(self):  return self.right  - self.left
    def height(self): return self.bottom - self.top


def main():
    global DISPLAY, CLOCK, LOGGER, update_sequence, status

    pygame.init()
    pygame.font.init()
    chat_module.init()
    logging_init()

    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    update_sequence = [[]]
    status = {'blinking': False,
              'last_blink': time.time(),
              'label': ''
              }

    normaleye1rect = pygame.Rect((WIDTH*0.41, HEIGHT*0.3, WIDTH*0.05, HEIGHT*0.27))
    normaleye2rect = pygame.Rect((WIDTH*0.54, HEIGHT*0.3, WIDTH*0.05, HEIGHT*0.27))
    face_rect = pygame.Rect(0, 0, HEIGHT / 2, HEIGHT / 2)
    face_rect.center = (WIDTH / 2, HEIGHT / 2)

    pygame.display.set_caption("CyberPet Gen.0")
    pygame.display.set_icon(image('icon.png'))

    while True:  # Game Loop
        # if update_sequence: print(update_sequence)
        DISPLAY.fill(GREY)
        onTop(pygame.display.get_wm_info()['window'])
        add_action(Action(draw_face, DISPLAY, face_rect))
        add_action(Action(draw_label, DISPLAY, status['label'], WHITE))
        if not status['blinking']:
            add_action(Action(draw_eyes, DISPLAY, normaleye1rect, normaleye2rect, BLACK, priority=1))
            if random.randint(0, 1000) + \
                    (int(time.time()-status['last_blink'])) >= 1000:
                random_blink(DISPLAY, normaleye1rect, normaleye2rect, 8)

        for event in pygame.event.get():  # Event loop
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if not status['blinking']:
                    random_blink(DISPLAY, normaleye1rect, normaleye2rect, 8)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    #print(ask_for_input())
                    update_status('label', f'...{chat_module.get_random_line()}...')
        do_next()
        pygame.display.flip()
        CLOCK.tick(FPS)


def image(path):
    return pygame.image.load(path).convert_alpha()


def draw_face(surface, face_rect):
    pygame.draw.rect(surface, WHITE, face_rect)
    pygame.draw.rect(surface, BLACK, face_rect, 5)
    return face_rect


def draw_eyes(surface, eye1rect, eye2rect, color):
    pygame.draw.rect(surface, color, eye1rect)
    pygame.draw.rect(surface, BLACK, eye1rect, 5)
    pygame.draw.rect(surface, color, eye2rect)
    pygame.draw.rect(surface, BLACK, eye2rect, 5)
    return eye1rect, eye2rect


def draw_label(surface:pygame.Surface, text, color, center=(WIDTH/2, HEIGHT/10)):
    font = pygame.font.SysFont('cambria', 15)
    if len(text.split()) > 12:
        text_surf1 = font.render(' '.join(text.split()[:13]), True, color)
        text_surf2 = font.render(' '.join(text.split()[13:]), True, color)
        text_rect1 = text_surf1.get_rect()
        text_rect2 = text_surf2.get_rect()
        text_rect1.center = center
        text_rect2.center = (center[0], text_rect1.bottom+3)
        surface.blit(text_surf1, text_rect1)
        surface.blit(text_surf2, text_rect2)
    else:
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        surface.blit(text_surf, text_rect)


def blink(surface, eye1rect, eye2rect, speed, offset=0):
    center1, center2 = eye1rect.center, eye2rect.center
    eye1rect_new, eye2rect_new = eye1rect.copy(), eye2rect.copy()
    init_w1, init_h1 = eye1rect_new.size
    init_w2, init_h2 = eye2rect_new.size
    add_action(Action(update_status, 'blinking', True), offset)
    for i in range(0, int(240/speed)):
        height_multiplier = math.sqrt(abs((i/120*speed)-1))  # y = √|x-1|, x∈[0,2]
        width_multiplier = -0.125*i/120 * (i/60-4) + 1  # y = -0.125x(x-4)+1, x∈[0,4]
        add_action(Action(draw_eyes, surface, eye1rect_new, eye2rect_new, BLACK, priority=1), i+offset)
        # Shapeshift the eyes
        eye1rect_new, eye2rect_new = eye1rect_new.copy(), eye2rect_new.copy()
        eye1rect_new.height, eye2rect_new.height = \
            init_h1*height_multiplier, init_h2*height_multiplier
        eye1rect_new.width, eye2rect_new.width = \
            init_w1*width_multiplier, init_w2*width_multiplier
        eye1rect_new.center, eye2rect_new.center = center1, center2
        # print(eye1rect_new.height, eye2rect_new.height)
    add_action(Action(update_status, 'blinking', False), int(240 / speed) + offset)


def blink_twice(surface, eye1rect, eye2rect, speed):
    blink(surface, eye1rect, eye2rect, speed)
    blink(surface, eye1rect, eye2rect, speed, offset=int(240/speed)+random.randint(1,30))
    # print('blink twice added')
    # print(update_sequence)


def random_blink(surface, eye1rect, eye2rect, speed):
    if random.randint(0, 1) == 0:
        blink_twice(surface, eye1rect, eye2rect, speed)
    else:
        blink(surface, eye1rect, eye2rect, speed)
    update_status('last_blink', time.time())


def add_action(action, frame:int=0):
    try:
        update_sequence[frame].append(action)
    except IndexError:
        update_sequence.append([action])


def do_next():
    try:
        action_sequence = sorted(update_sequence[0])
        for action in action_sequence:
            action.do()
        update_sequence.pop(0)
    except IndexError:
        return


def update_status(key, value):
    status[key] = value
    return key, value


def onTop(window):
    SetWindowPos = windll.user32.SetWindowPos
    GetWindowRect = windll.user32.GetWindowRect
    rc = RECT()
    GetWindowRect(window, byref(rc))
    SetWindowPos(window, -1, rc.left, rc.top, 0, 0, 0x0001)


def ask_for_input():
    popup = tk.Tk()
    label = tk.Label(popup, text="Nice to see you again.")
    entry = tk.Entry(popup)
    chatline = [None]

    def get_text(receiver):
        receiver[0] = entry.get()
        popup.destroy()
    button = tk.Button(popup, text="Enter", command=lambda:get_text(chatline))
    label.pack()
    entry.pack()
    button.pack()
    popup.mainloop()
    return chatline[0]


def logging_init():
    global LOGGER

    default_ch = logging.StreamHandler()  # Channel Handler
    default_fh = logging.FileHandler('PetLife!.log')
    default_ch.setLevel(logging.DEBUG)
    default_fh.setLevel(logging.DEBUG)
    LOGGER = logging.getLogger('CyberPet')
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(default_ch)
    LOGGER.addHandler(default_fh)


if __name__ == '__main__':
    main()
