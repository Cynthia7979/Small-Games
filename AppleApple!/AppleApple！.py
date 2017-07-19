import pygame, random, sys
from pygame.locals import *

costPerTree = 0
fullness = 20
blood = 20
pack = {}
screenWidth = 800
screenHeight = 600
WHITE = (255,255,255)
NAVYBLUE = (0,0,128)
SKYBLUE = (112,228,255)
BLACK = (0,0,0)

class Item(object):
    def __init__(self, itemName, isMaterial, isFood, isWeapon, isCraftable, cost, recipe=()):
        self.name = str(itemName)
        self.isMaterial = isMaterial
        self.isFood = isFood
        self.isWeapon = isWeapon
        self.Craftable = isCraftable
        self.cost = cost
        self.recipe = recipe


class Weapon(Item):
    def __init__(self, itemName, harm, cost, recipe):
        super(Weapon, self).__init__(itemName, False, False, True, True, cost, recipe)  # all weapons are craftable
        self.harm = harm


class Food(Item):
    def __init__(self, itemName, fullness, craftable, cost,recipe=(), isPotion=False, potionType=None, useDegree=None):
        super(Food,self).__init__(itemName, False, True, False, craftable, cost,recipe)
        self.fullness = fullness
        self.isPotion = isPotion
        self.type = potionType
        self.degree = useDegree

class Material(Item):
    def __init__(self, itemName, isCraftable, cost, recipe=()):
        super(Material,self).__init__(itemName, True, False, False, isCraftable, cost, recipe)


class Mob(object):
    def __init__(self, name, blood, damage, trophies):
        self.blood = blood
        self.damage = damage
        self.trophie = trophies
        self.name = name

# class Tool(Item):
#    def __init__(self,):
# Coming "soon"!!


# materials
wood = Material('wood', False, 3)

rock = Material('rock', False, 2)
feather = Material('feather', False, 2)
wool = Material('wool', False, 10)
stick = Material('stick', True, 1, (wood,))
copper = Material('copper ingot', True, 5, (rock, rock))
iron = Material('iron ingot', True, 12, (copper, copper, copper))
gold = Material('gold ingot', True, 27, (iron, iron, iron, iron))
diamond = Material('diamond!', True, 58, (gold, gold, gold, gold, gold))


# foods
flesh = Food('flesh', 2, False, 1)
berry = Food('blue berry', 5, False, 2)
egg = Food('egg', 1, False, 3)
milk = Food('a cup of milk', 10, False, 4)
wheat = Food('wheat', 3, False, 5)
flour = Food('flour', 1, True, 2, (wheat,))
cake = Food('cake', 20, True, 10, (egg, egg, milk, flour))

# mobs
zombie = Mob('zombie', 20, 1, (flesh,))
tree = Mob('tree', 10, 0.5, (wood, stick))
stone = Mob('stone', 30, 0.5, (rock,))
cow = Mob('cow', 25, 2, (milk, milk))
chicken = Mob('chicken', 15, 2.5, (egg, egg, feather))
sheep = Mob('sheep', 20, 1.5, (wool,))

# weapons
wooden_sword = Weapon('wooden sword', 2, 5, (wood, wood, stick))
stone_sword = Weapon('stone sword', 6, 12, (rock, rock, stick))
iron_sword = Weapon('iron sword', 18, 26, (iron, iron, stick))
golden_sword = Weapon('golden sword', 54, 54, (gold, gold, stick))
diamond_sword = Weapon('diamond sword', 162, 110, (diamond, diamond, stick))
better_wooden_sword = Weapon('better wooden sword', 10, 10, (wooden_sword, wooden_sword))  # and so on...

# places
placeToMobs = {'forest': (tree, tree, tree, tree, tree), 'farm': (cow, chicken, chicken, sheep)}


def main(): # so messy QAQ
    pygame.init()

    # load stats
    name,apple, appleTree, costPerTree, thingsToAdd = readFile()
    for thing in thingsToAdd:
        if thing in pack.keys():
            pack[thing] += 1
        else:
            pack[thing] = 1

    # variables
    DISPLAYSURF = pygame.display.set_mode((screenWidth,screenHeight))
    pygame.display.set_caption('Apple Apple!')
    currentScreen = 'main'
    tree = pygame.image.load('./tree.png')
    font = pygame.font.Font('arial.ttf',32)
    forest = pygame.image.load('./forest.png')
    farm = pygame.image.load('./farm.png')
    places = (forest,farm,forest,forest,forest,farm,farm,farm)

    # main loop
    while True:
        # draw screen
        if currentScreen == 'main':
            DISPLAYSURF.fill(SKYBLUE)
            x = 0
            for i in range(appleTree):
                DISPLAYSURF.blit(tree, (x, 420))
                x += 15
            exploreTextSurf = font.render('explore', True, WHITE, NAVYBLUE)
            exploreTextRect = exploreTextSurf.get_rect()
            exploreRect = pygame.Rect(670, 80, exploreTextRect.width, exploreTextRect.height)
            exploreTextRect.topleft = (670, 80)
            DISPLAYSURF.blit(exploreTextSurf, exploreTextRect)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    pos = event.pos
                    if pygame.Rect(pos[0], pos[1], 1, 1).colliderect(exploreRect):
                        currentScreen = 'explore choose'
        elif currentScreen == 'explore choose':
            if exploreChoosingScreen(DISPLAYSURF,font,places) == 'main':
                currentScreen = 'main'

        # draw apple bar
        appleImg = pygame.image.load('./apple.png')
        DISPLAYSURF.blit(appleImg,(0,0))
        appleTextSurface = font.render(':' + str(apple), True, BLACK)
        appleTextRect = appleTextSurface.get_rect()
        appleTextRect.topleft = (60, 10)
        DISPLAYSURF.blit(appleTextSurface,appleTextRect)

        # event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()



        pygame.display.update()


def readFile():
    f = open('.\UsrStat.txt')
    texts = f.read()
    category = texts.split('\n\n')
    details = []
    for part in category:
        splited = part.split('\n')
        for s in splited:
            # print s
            n = s.find('#')
            if n != -1:
                s = s[:n]
            details.append(s)
            # print s
    pack = details[4:]
    return details[0], int(details[1]), int(details[2]), int(details[3]), pack


def pickApple(appleTree):
    tuple = (False, False, True)
    doExtra = random.choice(tuple)
    if doExtra:
        applePerTree = 5
    else:
        applePerTree = 3
    return appleTree * applePerTree


def buyJustice(money, thing):
    if thing.cost > money:
        return False
    else:
        return True


def plantTreeJustice(num, apple):
    if num*costPerTree < apple:
        return True
    else:
        return False


def exploreChoosingScreen(DISPLAYSURF,font,places):
    DISPLAYSURF.fill(WHITE)
    questionSurf = font.render('Please choose the place to go', True, BLACK)
    questionRect = questionSurf.get_rect()
    questionRect.center = (400, 50)
    DISPLAYSURF.blit(questionSurf, questionRect)

    backTextSurf = font.render('back', True, WHITE, NAVYBLUE)
    backTextRect = backTextSurf.get_rect()
    backButtonRect = pygame.Rect(700, 500, backTextRect.width, backTextRect.height)
    backTextRect.topleft = (700, 500)
    DISPLAYSURF.blit(backTextSurf, backTextRect)
    x = 50
    y = 100
    for place in places:
       DISPLAYSURF.blit(place, (x, y))
       x += 150
       if x >= 800:
            y += 150
            x = 50
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            x,y = event.pos
            if pygame.Rect(x,y,1,1).colliderect(backButtonRect):
                print 'back!'
                return 'main'
        elif event.type == QUIT:
            pygame.quit()
if __name__ == '__main__':
    main()
