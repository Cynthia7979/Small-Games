import pygame


class Target:
    def __init__(self, *args):
        self.name = args[0]
        self.info = args[1]
        self.parent = args[2]
        self.children = args[3]
        self.image = args[4]
        self.pos = args[5]
        self.x = self.pos[0]
        self.y = self.pos[1]

    def __str__(self):
        return """name: %s,
                info: %s"""


def main():
    pass


def run_game():
    pass


def read_file():
    f = open('./data.fa2s')
    targets = {}
    raw_data = f.read()
    for obj in raw_data.split('-\n'):
        props = []
        for prop in obj.split('\n'):
            props.append(prop)
        targets[props[0]] = Target(props)

    return targets


read_file()

