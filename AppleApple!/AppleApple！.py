import pygame, random, sys
from pygame.locals import *

costPerTree = 0
fullness = 20
blood = 20
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


# item initalizing
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


def main():
    pygame.init()
    pack = {}


    # load stats from file
    name, apple, appleTree, costPerTree, thingsToAdd = readFile()
    # add thing to pack
    for thing in thingsToAdd:
        if thing in pack.keys():
            pack[thing] += 1
        else:
            pack[thing] = 1
    # print thing
    # initalizing
    DISPLAYSURF = pygame.display.set_mode((screenWidth,screenHeight))
    pygame.display.set_caption('Apple Apple!')
    currentScreen = 'main'
    currentItem = 0
    weaponInUse = wooden_sword
    tipText = 'Arriving ...'
    # load images
    tree = pygame.image.load('./tree.png')
    font = pygame.font.Font('arial.ttf',32)
    forest = pygame.image.load('./forest.png')
    farm = pygame.image.load('./farm.png')
    places = {'forest':forest,'farm':farm}
    # load and set apple icon
    appleImg = pygame.image.load('./apple.png')
    appleImgRect = appleImg.get_rect()
    appleImgRect.topleft = (0, 0)

    # main loop
    while True:
        # set apple bar
        appleTextSurface = font.render(':' + str(apple), True, BLACK)
        appleTextRect = appleTextSurface.get_rect()
        appleTextRect.topleft = (60, 10)

        # draw screen
        if currentScreen == 'main': # main screen
            DISPLAYSURF.fill(SKYBLUE)
            x = 0
            for i in range(appleTree):
                DISPLAYSURF.blit(tree, (x, 420))
                x += 15
            # explore button
            exploreTextSurf = font.render('explore', True, WHITE, NAVYBLUE)
            exploreTextRect = exploreTextSurf.get_rect()
            exploreRect = pygame.Rect(670, 80, exploreTextRect.width, exploreTextRect.height)
            exploreTextRect.topleft = (670, 80)
            DISPLAYSURF.blit(exploreTextSurf, exploreTextRect)
            # pack button
            packTextSurf = font.render('pack', True, WHITE, NAVYBLUE)
            packTextRect = exploreTextSurf.get_rect()
            packRect = pygame.Rect(670, 150, packTextRect.width, packTextRect.height)
            packTextRect.topleft = (670,150)
            DISPLAYSURF.blit(packTextSurf, packTextRect)
            # event handling loop
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    x,y = event.pos
                    if pygame.Rect(x,y, 1, 1).colliderect(exploreRect): # clicked explore button
                        currentScreen = 'explore choose'
                    elif pygame.Rect(x,y,1,1).colliderect(packRect): # clicked pack button
                        currentScreen = 'pack'
                    elif pygame.Rect(x,y,1,1).colliderect(appleImgRect): # clicked apple icon (to pick apple)
                        apple += pickApple(appleTree)
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
        elif currentScreen == 'explore choose': # explore destination choosing screen
            thingReturned = exploreChoosingScreen(DISPLAYSURF,font,places)
            if thingReturned: # returned something
                if thingReturned == 'main': # go back
                    currentScreen = 'main'
                elif thingReturned[:4] == 'goto': # explore somewhere
                    currentScreen = 'place' + thingReturned[4:]
                    #while True:
                        #print thingReturned[4:]
                    #currentScreen = 'main'
        elif currentScreen == 'pack': # pack viewing and managing screen
            do, back = packScreen(DISPLAYSURF,font,pack,currentItem) # to switch item or not and go back or not
            if currentItem < len(pack)-1 and currentItem > -len(pack): # not out of range
                currentItem += do
            else:
                currentItem = 0 # start over
            if back:
                currentScreen = 'main' # go back
        elif currentScreen[:5] == 'place': # exploring screen, working on
            DISPLAYSURF.fill(SKYBLUE)
            place = currentScreen[5:] # cut the place string
            mobs = placeToMobs[place] # get mobs to fight against
            # draw tip text
            tipTextSurface = font.render(tipText,True,BLACK)
            tipTextRect = tipTextSurface.get_rect()
            tipTextRect.center = (400,50)
            DISPLAYSURF.blit(tipTextSurface,tipTextRect)
            # draw health (blood) icon
            bloodIcon = pygame.image.load('./bloodIcon.png')
            DISPLAYSURF.blit(bloodIcon,(0,80))
            # draw health (blood) measure (how many)
            bloodTextSurf = font.render(': ' + str(blood),True,BLACK)
            bloodTextRect = bloodTextSurf.get_rect()
            bloodTextRect.topleft = (60,80)
            DISPLAYSURF.blit(bloodTextSurf,bloodTextRect)
            # initalize current mob
            currentMob = 0
            # TODO: fighting with mob and get things system


        # draw apple bar
        DISPLAYSURF.blit(appleImg, (0, 0))
        DISPLAYSURF.blit(appleTextSurface,appleTextRect)

        # event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()



        pygame.display.update() # update the window



def packScreen(DISPLAYSURF,font,pack,currentItem):
    do = 0 # switch the item
    back = False # go back to home page?

    DISPLAYSURF.fill(WHITE)
    # draw 'Pack' title
    titleSurf = font.render('Pack',True,BLACK)
    titleRect = titleSurf.get_rect()
    titleRect.center = (400,50)
    DISPLAYSURF.blit(titleSurf,titleRect)
    # draw arrows
    leftArrow = pygame.image.load('./left.png')
    leftRect = leftArrow.get_rect()
    leftRect.topleft = (100,250)
    rightArrow = pygame.image.load('./right.png')
    rightRect = rightArrow.get_rect()
    rightRect.topleft = (600,250)
    DISPLAYSURF.blit(leftArrow,(100,250))
    DISPLAYSURF.blit(rightArrow,(600,250))
    # draw back button
    backTextSurf = font.render('back', True, WHITE, NAVYBLUE)
    backTextRect = backTextSurf.get_rect()
    backButtonRect = pygame.Rect(700, 500, backTextRect.width, backTextRect.height)
    backTextRect.topleft = (700, 500)
    DISPLAYSURF.blit(backTextSurf, backTextRect)

#    x = 50
#    y = 100
#    for item in pack.keys():
#        itemSurf = font.render(item,True,BLACK)
#        itemRect = itemSurf.get_rect()
#        if x + itemRect.width > screenWidth:
#            x = 50
#            y += 100
#        itemRect.topleft = (x,y)
#        x += itemRect.width + 50
#        if x >= screenWidth:
#            y += 100
#            x = 50
#        DISPLAYSURF.blit(itemSurf,itemRect)
    itemTexts = {}
    for item in pack.keys():
        # set item name and number (how many of the item)
        itemSurf = font.render(item, True, BLACK)
        itemRect = itemSurf.get_rect()
        itemRect.center = (400,300)
        numSurf = font.render(str(pack[item]),True,BLACK)
        numRect = numSurf.get_rect()
        numRect.topleft = (500,250)
        itemTexts[item] = [itemSurf,itemRect,numSurf,numRect]
# item surf;rect,number surf;rect
    isurf,irect,nsurf,nrect = itemTexts[itemTexts.keys()[currentItem]] # change to current item name
    DISPLAYSURF.blit(isurf,irect)
    # event handling loop
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            x,y = event.pos
            if pygame.Rect(x,y,1,1).colliderect(leftRect):
                do = -1
            elif pygame.Rect(x,y,1,1).colliderect(rightRect):
                do = 1
            elif pygame.Rect(x,y,1,1).colliderect(backButtonRect):
                back = True
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    return (do,back)
    # FIXME: if you only press left or right you may skip something...

def readFile():
    f = open('.\UsrStat.txt')
    texts = f.read()
    category = texts.split('\n\n') # player stats and pack things
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
    #       playername       apple       apple tree   apple cost per tree
    return details[0], int(details[1]), int(details[2]), int(details[3]), pack


def pickApple(appleTree):
    tuple = (False, False, True) # percent to have extra apple
    doExtra = random.choice(tuple) # decide if to have extra apple
    if doExtra:
        applePerTree = 5
    else:
        applePerTree = 3
    return appleTree * applePerTree


def buyJustice(apple, thing):
    if thing.cost > apple:
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
    # set question texts
    questionSurf = font.render('Please choose the place to go', True, BLACK)
    questionRect = questionSurf.get_rect()
    questionRect.center = (400, 50)
    DISPLAYSURF.blit(questionSurf, questionRect)
    # set back button
    backTextSurf = font.render('back', True, WHITE, NAVYBLUE)
    backTextRect = backTextSurf.get_rect()
    backButtonRect = pygame.Rect(700, 500, backTextRect.width, backTextRect.height)
    backTextRect.topleft = (700, 500)
    DISPLAYSURF.blit(backTextSurf, backTextRect)
    # initalize x and y
    x = 50
    y = 100
    placeRects = {}
    for place in places.keys():
        # set place image
        placeSurf = places[place]
        placeRect = placeSurf.get_rect()
        placeRect.topleft = (x,y)
        placeRects[place] = ((placeSurf,placeRect))
        DISPLAYSURF.blit(placeSurf,placeRect)
        x += 150
        if x >= 800:
            y += 150
            x = 50
    # event handling loop
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            x,y = event.pos
            if pygame.Rect(x,y,1,1).colliderect(backButtonRect): # back button
                #print 'back!'
                return 'main'
            for place in placeRects.keys():
                if pygame.Rect(x,y,1,1).colliderect(placeRects[place][1]): # go to this place
                    return 'goto' + place

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
