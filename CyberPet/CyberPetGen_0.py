# TODO: Make it possible to pass `status name` as argument 我疯了
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
CENTER = (WIDTH/2, HEIGHT/2)
FPS = 60

#        R   G   B
GREY  = (80 , 80 , 80 )
BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
RED   = (255, 0,   0)

LOGGING_LEVEL = logging.INFO


# Syntax Sugars
RECT, SURF, DEFAULT_RECT = 0, 1, 2


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
            LOGGER.error(f'{e.__class__.__name__}: {self}')
            raise e

    def __repr__(self):
        return self.func.__name__ + str(self.args)

    def __gt__(self, other):
        return self.priority > other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __eq__(self, other):
        return self.priority == other.priority


class RECT_(Structure):
    _fields_ = [
    ('left',    c_long),
    ('top',     c_long),
    ('right',   c_long),
    ('bottom',  c_long),
    ]
    def width(self):  return self.right  - self.left
    def height(self): return self.bottom - self.top


def main():
    global DISPLAY, CLOCK, LOGGER, update_sequence, status, draggables

    pygame.init()
    pygame.font.init()
    chat_module.init()
    logging_init()

    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    update_sequence = [[]]
    status = {'blinking': False,
              'showing_comfort': False,
              'last_blink': time.time(),
              'label': '',
              'eye1rect': None,  # Will be defined later by get_eye_rects()
              'eye2rect': None,
              'eye_margin': WIDTH*0.08,
              'eyes_rect': pygame.Rect((WIDTH*0.41, HEIGHT*0.3, WIDTH*0.18, HEIGHT*0.27)),
              'eyes_center': None,  # Will be defined in the code below
              'mouse_pos_down': None,
              'widget_currently_dragging': None
              }
    draggables = {'testFood': image('testFood.png', default_rect=True, topleft=(0,0))}
    #                         tuple of (rect, surf)

    # normaleye1rect = pygame.Rect((WIDTH*0.41, HEIGHT*0.3, WIDTH*0.05, HEIGHT*0.27))
    # normaleye2rect = pygame.Rect((WIDTH*0.54, HEIGHT*0.3, WIDTH*0.05, HEIGHT*0.27))
    # status['eyes_rect'] = pygame.Rect((normaleye1rect.left, normaleye1rect.top,
    #                               normaleye2rect.right-normaleye1rect.left,
    #                               normaleye1rect.height))
    status['eyes_center'] = status['eyes_rect'].center
    update_eye_rects(status['eyes_rect'], status['eye_margin'])
    face_rect = pygame.Rect(0, 0, HEIGHT / 2, HEIGHT / 2)
    face_rect.center = CENTER


    pygame.display.set_caption("CyberPet Gen.0")
    pygame.display.set_icon(image('icon.png'))

    # --------------- INSERT DEBUG CODE HERE ---------------------
    # print(pygame.Rect((WIDTH*0.41, HEIGHT*0.3, WIDTH*0.05, HEIGHT*0.27)),
    #       pygame.Rect((WIDTH*0.54, HEIGHT*0.3, WIDTH*0.05, HEIGHT*0.27)))
    # ----------------- END OF DEBUG RANGE -----------------------

    while True:  # Game Loop
        DISPLAY.fill(GREY)
        onTop(pygame.display.get_wm_info()['window'])
        do_next()

        add_action(draw_widgets, DISPLAY)

        # Collision-related conditionals
        if draggables['testFood'][RECT].colliderect(face_rect):
            draggables['testFood'][RECT] = draggables['testFood'][DEFAULT_RECT].copy()
            show_comfort(DISPLAY, face_rect)
            stop_dragging()

        # Status-related conditionals
        if status['label']:
            add_action(draw_label, DISPLAY, status['label'], WHITE)
        if not status['blinking']:
            add_action(draw_eyes, DISPLAY, status['eye1rect'], status['eye2rect'], BLACK, priority=1)
            if not (status['showing_comfort'] or status['widget_currently_dragging']):
                if random.randint(0, 1000) + \
                        (int(time.time()-status['last_blink'])) >= 1000:
                    random_blink(DISPLAY, status['eye1rect'], status['eye2rect'], [5,6,7])
        if not status['showing_comfort']:
            add_action(draw_face, DISPLAY, face_rect)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    #print(ask_for_input())
                    update_status('label', f'...{chat_module.get_random_line()}...')
            if event.type == pygame.MOUSEMOTION:
                # Look at the mouse
                mouse_pos = pygame.mouse.get_pos()
                x_diff, y_diff = (mouse_pos[i] - CENTER[i] for i in (0,1))
                new_center = (status['eyes_center'][0]+x_diff//15, status['eyes_center'][1]+y_diff//30)
                status['eyes_rect'].center = new_center
                update_eye_rects(status['eyes_rect'], int(status['eye_margin']))

                # Move widgets
                if status['widget_currently_dragging']:
                    ori_wid_x, ori_wid_y = draggables[status['widget_currently_dragging']][RECT].topleft
                    ori_mouse_x, ori_mouse_y = status['mouse_pos_down']
                    new_mouse_x, new_mouse_y = mouse_pos
                    change_x = new_mouse_x-ori_mouse_x
                    change_y = new_mouse_y-ori_mouse_y
                    draggables[status['widget_currently_dragging']][RECT].topleft = ori_wid_x+change_x, ori_wid_y+change_y
                    update_status('mouse_pos_down', mouse_pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                LOGGER.info('Mouse Button Down')
                mouse_pos = event.pos
                if not status['mouse_pos_down']:
                    update_status('mouse_pos_down', mouse_pos)
                    for w_name, (w_rect, r_surf, _) in draggables.items():
                        if w_rect.collidepoint(mouse_pos):
                            update_status('widget_currently_dragging', w_name)
            if event.type == pygame.MOUSEBUTTONUP:
                LOGGER.info('Mouse Button Up')
                if status['widget_currently_dragging']:
                    stop_dragging()
                else:
                    if not status['blinking']:
                        random_blink(DISPLAY, status['eye1rect'], status['eye2rect'], [5, 6, 7])
        # --------------- INSERT DEBUG CODE HERE ---------------------
        # pygame.draw.rect(DISPLAY, RED, status['eyes_rect'])
        print(status['eyes_rect'])
        # ----------------- END OF DEBUG RANGE -----------------------
        pygame.display.flip()
        CLOCK.tick(FPS)


# ------------ Draw Related ------------


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


def draw_widgets(surface):
    for (w_rect, w_surf, _) in draggables.values():
        surface.blit(w_surf, w_rect)

# ------------ Animation Related ------------


def blink(surface, eye1rect, eye2rect, speed, offset=0, stop_blinking=True):
    center1, center2 = eye1rect.center, eye2rect.center
    eye1rect_new, eye2rect_new = eye1rect.copy(), eye2rect.copy()
    init_w1, init_h1 = eye1rect_new.size
    init_w2, init_h2 = eye2rect_new.size
    add_action(update_status, 'blinking', True, frame=offset)
    for i in range(0, int(240/speed)):
        height_multiplier = math.sqrt(abs((i/120*speed)-1))  # y = √|x-1|, x∈[0,2]
        width_multiplier = -0.125*i/120 * (i/60-4) + 1  # y = -0.125x(x-4)+1, x∈[0,4]
        add_action(draw_eyes, surface, eye1rect_new, eye2rect_new, BLACK, frame=i+offset, priority=1)
        # Shapeshift the eyes
        eye1rect_new, eye2rect_new = eye1rect_new.copy(), eye2rect_new.copy()
        eye1rect_new.height, eye2rect_new.height = \
            init_h1*height_multiplier, init_h2*height_multiplier
        eye1rect_new.width, eye2rect_new.width = \
            init_w1*width_multiplier, init_w2*width_multiplier
        eye1rect_new.center, eye2rect_new.center = center1, center2
        # print(eye1rect_new.height, eye2rect_new.height)
    if stop_blinking: add_action(update_status, 'blinking', False, frame=int(240 / speed) +offset-1)


def blink_twice(surface, eye1rect, eye2rect, speed):
    blink(surface, eye1rect, eye2rect, speed, stop_blinking=False)
    blink(surface, eye1rect, eye2rect, speed, offset=int(240/speed)+random.randint(1,30))
    # print('blink twice added')
    # print(update_sequence)


def random_blink(surface, eye1rect, eye2rect, speed):
    speed = random.choice(speed)
    if random.randint(0, 1) == 0:
        blink_twice(surface, eye1rect, eye2rect, speed)
    else:
        blink(surface, eye1rect, eye2rect, speed)
    update_status('last_blink', time.time())


def show_comfort(surface, face_rect):  # TODO
    # First become thinner and taller,
    # Then become fatter and shorter
    # As if it was a slime
    # At last go back to normal
    midbottom = face_rect.midbottom
    init_w, init_h = face_rect.size
    init_eye_x, init_eye_y = status['eyes_center']
    face_rect_new = face_rect.copy()
    add_action(update_status, 'showing_comfort', True)
    for t in range(0, 30):  # fh=0.3ht/30+h, fw=-0.1wt/30+w, f_e=0.1yt/30+y
        # This time I'm not using multipliers. Instead, the y values are directly used as heights
        add_action(draw_face, surface, face_rect_new.copy(), frame=t)
        f_h = lambda t: 0.3*init_h*t/30+init_h
        f_w = lambda t: -0.1*init_w*t/30+init_w
        f_eye = lambda t: 0.1*init_eye_y*t/30+init_eye_y
        face_rect_new.size = (f_w(t), f_h(t))
        face_rect_new.midbottom = midbottom
        # TODO The following three steps should be packed together
        add_action(update_status, 'eyes_center', (init_eye_x, f_eye(t)), frame=t)
        status['eyes_rect'].center = status['eyes_center']
        add_action(update_eye_rects, status['eyes_rect'], status['eye_margin'], frame=t)
    for t in range(0, 30):  # fh=-0.3ht/30+1.5h, fw=0.1wt/30+w
        add_action(draw_face, surface, face_rect_new.copy(), frame=t+30)
        f_h = lambda t: -0.3*init_h*t/30 + 1.3*init_h
        f_w = lambda t: 0.1*init_w*t/30 + 0.9*init_w
        f_eye = lambda t: -0.1*init_eye_y*t/30 + 1.1*init_eye_y
        face_rect_new.size = (f_w(t), f_h(t))
        face_rect_new.midbottom = midbottom
        add_action(update_status, 'eyes_center', (init_eye_x, f_eye(t)), frame=t+30)
        status['eyes_rect'].center = status['eyes_center']
        add_action(update_eye_rects, status['eyes_rect'], status['eye_margin'], frame=t+30)
    add_action(update_status, 'showing_comfort', False, frame=60)
    pass

# ------------ Action Related ------------


def add_action(func, *args, priority=0, frame:int=0):
    action = Action(func, *args, priority=priority)
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


def update_eye_rects(eyesrect, margin):
    eye1rect, eye2rect = get_eye_rects(eyesrect, margin)
    update_status('eye1rect', eye1rect)
    update_status('eye2rect', eye2rect)

# ------------ Misc ------------


def image(path, rect=False, default_rect=False, topleft=(0,0)):
    img = pygame.image.load(path).convert_alpha()
    img_rect = img.get_rect()
    img_rect.topleft = topleft
    img_default_rect = img_rect.copy()
    if default_rect:
        return [img_rect, img, img_default_rect]
    elif rect:
        return [img_rect, img]
    return img


def onTop(window):
    SetWindowPos = windll.user32.SetWindowPos
    GetWindowRect = windll.user32.GetWindowRect
    rc = RECT_()
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
    default_ch.setLevel(LOGGING_LEVEL)
    default_fh.setLevel(LOGGING_LEVEL)
    LOGGER = logging.getLogger('CyberPet')
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(default_ch)
    LOGGER.addHandler(default_fh)


def stop_dragging():
    update_status('mouse_pos_down', None)
    update_status('widget_currently_dragging', None)
    update_status('drag_pos_diff', (None, None))


def get_eye_rects(eyesrect:pygame.Rect, margin):
    #LOGGER.debug(f'Getting eyerects using {eyesrect} and margin {margin}...')
    eye1rect = pygame.Rect(eyesrect.left, eyesrect.top, eyesrect.centerx-margin/2-eyesrect.left, eyesrect.height)
    eye2rect = pygame.Rect(eyesrect.centerx+margin/2, eyesrect.top, eyesrect.right-eyesrect.centerx-margin/2, eyesrect.height)
    #print(eye1rect, eye2rect)
    return eye1rect, eye2rect


if __name__ == '__main__':
    main()
