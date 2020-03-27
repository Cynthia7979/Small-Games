import pygame
import sys
import random
from ctypes import windll, Structure, c_long, byref  # Keep on top

WIDTH, HEIGHT = 480, 360
CENTER = (WIDTH/2, HEIGHT/2)
BLACK = (0,0,0)
WHITE = (255,255,255)


class RECT(Structure):  # 直接从CyberPet搬过来
    _fields_ = [
    ('left',    c_long),
    ('top',     c_long),
    ('right',   c_long),
    ('bottom',  c_long),
    ]
    def width(self):  return self.right  - self.left
    def height(self): return self.bottom - self.top


def main():
    global LARGER_FONT, SMALLER_FONT, CLOCK, FPS, DISPLAY
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('BREATHE')
    pygame.display.set_icon(pygame.image.load('breathe.png'))

    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60
    LARGER_FONT = pygame.font.SysFont('Microsoft YaHei', 132)
    SMALLER_FONT = pygame.font.SysFont('Microsoft YaHei', 64)

    POWER_BREATHING_SEQUENCE = [('INHALE', 4), ('EXHALE', 8)]
    FOUR_SEVEN_EIGHT_SEQUENCE = [('INHALE', 4), ('HOLD', 7), ('EXHALE', 8)]
    EQUAL_BREATHING_SEQUENCE = [('INHALE', 5), ('EXHALE', 5)]

    DICT_OF_SEQUENCE = {'Power Breathing': POWER_BREATHING_SEQUENCE, '4-7-8 Breathing': FOUR_SEVEN_EIGHT_SEQUENCE,
                        'Equal Breathing': EQUAL_BREATHING_SEQUENCE}
    LIST_OF_SEQUENCE = list(DICT_OF_SEQUENCE.keys())

    number_banner, number_rect = banner(0)
    label, label_rect = banner('', upper=True)

    print('Please choose a sequence, Enter for random:')
    for i, seq in enumerate(LIST_OF_SEQUENCE):
        print(f'  {i}. {seq}')
    try:
        choice = LIST_OF_SEQUENCE[int(input('>'))]
        SEQUENCE = DICT_OF_SEQUENCE[choice]
    except (KeyError, ValueError):
        choice = random.choice(LIST_OF_SEQUENCE)
        SEQUENCE = DICT_OF_SEQUENCE[choice]
    print('Presenting:', choice)

    while True:
        for label_text, length in SEQUENCE:
            label, label_rect = banner(label_text, upper=True)
            for second in range(1, length+1):
                for frame in range(FPS):
                    if frame == 0:
                        number_banner, number_rect = banner(second)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    DISPLAY.fill(WHITE)
                    DISPLAY.blit(label, label_rect)
                    DISPLAY.blit(number_banner, number_rect)
                    onTop(pygame.display.get_wm_info()['window'])
                    pygame.display.flip()
                    CLOCK.tick(FPS)


def banner(text, upper=False):
    if upper:
        text = SMALLER_FONT.render(text, True, BLACK)
        rect = text.get_rect()
        rect.center = (WIDTH/2, HEIGHT/1.25)
    else:
        text = LARGER_FONT.render(str(text), True, BLACK)
        rect = text.get_rect()
        rect.center = CENTER
    return text, rect


def onTop(window):
    SetWindowPos = windll.user32.SetWindowPos
    GetWindowRect = windll.user32.GetWindowRect
    rc = RECT()
    GetWindowRect(window, byref(rc))
    SetWindowPos(window, -1, rc.left, rc.top, 0, 0, 0x0001)


if __name__ == '__main__':
    main()
