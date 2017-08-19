import pygame, random, sys, pickle
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
CLOCK = pygame.time.Clock()
FPS = 20

class Item(object):
    def __init__(self, itemName, isMaterial, isFood, isWeapon, isCraftable, cost, recipe=()):
        self.name = str(itemName)
        self.isMaterial = isMaterial
        self.isFood = isFood
        self.isWeapon = isWeapon
        self.Craftable = isCraftable
        self.cost = cost
        self.recipe = recipe
# TODO: change every type() or isinstance to: if item.isMaterial...

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
placeToMobs = {'forest': (tree, tree, tree, tree, tree), 'farm': (tree, stone, tree, stone)}


def main():
    pygame.init()
    pack = {}
    # load stats from file
    name, apple, appleTree, costPerTree, startBlood, thingsToAdd = readFile()
    global name, apple, appleTree, costPerTree, startBlood, pack
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
    storeCurrentItem = 0
    weaponInUse = wooden_sword
    tipText = ''
    currentLand = 0
    mobBlood = None
    mobs = None
    playerBlood = startBlood
    thingsCanBuy = [[berry,berry,milk,flour,wooden_sword]]
    thingsNowOn = []
    # load images
    tree = pygame.image.load('./tree.png')
    font = pygame.font.Font('arial.ttf',32)
    forest = pygame.image.load('./forest.png')
    farm = pygame.image.load('./farm.png')
    places = {'forest':forest,'farm':farm}
    land1 = pygame.image.load('./land.png')
    land2 = pygame.image.load('./landAnimated.png')
    lands = (land1, land2)
    # load and set apple icon
    appleImg = pygame.image.load('./apple.png')
    appleImgRect = appleImg.get_rect()
    appleImgRect.topleft = (0, 0)

    # main loop
    while True: # TODO: make up saving system, 'plant tree' function
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
            exploreRect = placeButton(DISPLAYSURF,font,'explore',670,80)
            # pack button
            packRect = placeButton(DISPLAYSURF,font,'pack',670,150)
            # plant tree button
            plantRect = placeButton(DISPLAYSURF,font,'plant tree',650,220)
            # apple farm text
            farmTextSurf = font.render('This is ' + name + "'s apple farm", True, BLACK)
            farmTextRect = farmTextSurf.get_rect()
            farmTextRect.center = (400,50)
            DISPLAYSURF.blit(farmTextSurf,farmTextRect)
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
                    elif pygame.Rect(x,y,1,1).colliderect(plantRect):
                        if appleTree < 50:
                            appleTree += 1
                            apple -= costPerTree
                            costPerTree += 1
                elif event.type == QUIT:
                    save(name, apple, appleTree, costPerTree, startBlood, pack)
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
            do, back, screen, weapon, sell = packScreen(DISPLAYSURF,font,pack,currentItem) # to switch item or not and go back or not
            if currentItem < len(pack)-1 and currentItem > -1 * (len(pack)): # not out of range
                currentItem += do
            else:
                currentItem = 0 # start over
            if back:
                currentScreen = 'main' # go back
            if screen:
                currentScreen = screen
            if weapon:
                if isinstance(weapon,Weapon):
                    weaponInUse = weapon
            if sell:
                if len(pack.keys()) <= 1:
                    pass
                else:
                    for item in pack.keys():
                        if item == sell:
                            apple += item.cost
                            if pack[item] == 1:
                                del pack[item]
                            else:
                                pack[item] -= 1
                            currentItem += 1
        elif currentScreen[:5] == 'place': # exploring screen, working on
            DISPLAYSURF.fill(SKYBLUE)
            place = currentScreen[5:] # cut the place string
            if not mobs:
                mobs = list(placeToMobs[place]) # get mobs to fight against
                #for mob in mobs:
                #    print mob.name
            # draw tip text
            tipTextSurface = font.render(tipText,True,BLACK)
            tipTextRect = tipTextSurface.get_rect()
            tipTextRect.center = (400,50)
            DISPLAYSURF.blit(tipTextSurface,tipTextRect)
            # draw health (blood) icon
            bloodIcon = pygame.image.load('./bloodIcon.png')
            DISPLAYSURF.blit(bloodIcon,(0,80)) # player's
            DISPLAYSURF.blit(bloodIcon,(650,80)) # mob's
            # draw land
            DISPLAYSURF.blit(lands[currentLand % 2],(0,500))
            currentLand += 1
            # draw health (blood) measure (how many) - player
            playerbloodTextSurf = font.render(': ' + str(playerBlood),True,BLACK)
            playerbloodTextRect = playerbloodTextSurf.get_rect()
            playerbloodTextRect.topleft = (60,80)
            DISPLAYSURF.blit(playerbloodTextSurf,playerbloodTextRect)
            # get mob stat
            mob = mobs[0]
            if mobBlood == None:
                mobBlood = mob.blood
            # draw health measure - mob
            mobBloodTextSurf = font.render(': ' + str(mobBlood),True,BLACK)
            mobBloodTextRect = playerbloodTextSurf.get_rect()
            mobBloodTextRect.topleft = (710,80)
            DISPLAYSURF.blit(mobBloodTextSurf,mobBloodTextRect)
            tipText = 'fighting with ' + mob.name
            mobBlood -= weaponInUse.harm
            pygame.time.wait(500)
            playerBlood -= mob.damage
            if playerBlood <= 0: # defeated
                currentScreen = 'main'
                playerBlood = 0
            if mobBlood <= 0: # this mob defeated
                for trophie in mob.trophie:
                    if trophie in pack.keys():
                        pack[trophie] += 1
                    else:
                        pack[trophie] = 1
                mobBlood = None
                del mobs[0]
                #for mob in mobs:
                    #print mob.name
            if mobs == []: # victory
                currentScreen = 'main'
        elif currentScreen == 'store':
            if thingsNowOn == []:
                thingsNowOn = random.choice(thingsCanBuy)
            do,back,buy = storeScreen(DISPLAYSURF,font,thingsNowOn,storeCurrentItem,apple)
            storeCurrentItem += do
            if back:
                currentScreen = 'pack'
            if storeCurrentItem < 0:
                storeCurrentItem = len(thingsNowOn) - 1
            if buy:
                if buyJustice(apple,buy):
                    apple -= buy.cost
                    if buy in pack.keys():
                        pack[buy] += 1
                    else:
                        pack[buy] = 1
            # FIXME: if you press back button, you will switch the item?

        # draw apple bar
        DISPLAYSURF.blit(appleImg, (0, 0))
        DISPLAYSURF.blit(appleTextSurface,appleTextRect)

        # event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                save(name,apple,appleTree,costPerTree,startBlood,pack)
                pygame.quit()
                sys.exit()


        CLOCK.tick(FPS)
        pygame.display.update() # update the window


def packScreen(DISPLAYSURF,font,pack,currentItem):
    do = 0 # switch the item
    back = False # go back to home page?
    screen = None # go to which screen?
    weapon = None
    sell = None # if sell something it will become the thing

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
    #backTextSurf = font.render('back', True, WHITE, NAVYBLUE)
    #backTextRect = backTextSurf.get_rect()
    #backButtonRect = pygame.Rect(700, 500, backTextRect.width, backTextRect.height)
    #backTextRect.topleft = (700, 500)
    #DISPLAYSURF.blit(backTextSurf, backTextRect)\
    backButtonRect = placeButton(DISPLAYSURF, font, 'back', 650, 500)

    # draw sell button
    #sellTextSurf = font.render('sell', True, WHITE, NAVYBLUE)
    #sellTextRect = sellTextSurf.get_rect()
    #sellButtonRect = pygame.Rect(420, 500, sellTextRect.width, sellTextRect.height)
    #sellTextRect.topleft = (420, 500)
    #DISPLAYSURF.blit(sellTextSurf, sellTextRect)
    sellButtonRect = placeButton(DISPLAYSURF, font, 'sell', 110, 500)

    # draw store button
    #sellTextSurf = font.render('back', True, WHITE, NAVYBLUE)
    #sellTextRect = sellTextSurf.get_rect()
    #sellButtonRect = pygame.Rect(420, 500, storeTextRect.width, storeTextRect.height)
    #sellTextRect.topleft = (420, 500)
    #DISPLAYSURF.blit(storeTextSurf, storeTextRect)
    storeButtonRect = placeButton(DISPLAYSURF, font, 'store', 310, 500)

    # draw equip button
    equipButtonRect = placeButton(DISPLAYSURF, font, 'equip', 470, 500)
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

    itemNames = []
    for item in pack.keys():
        itemNames.append(item.name)
    itemTexts = {}
    for itemName in itemNames:
        # set item name and number (how many of the item)
        itemSurf = font.render(itemName, True, BLACK)
        itemRect = itemSurf.get_rect()
        itemRect.center = (400,300)
        numSurf = font.render(str(pack.values()[itemNames.index(itemName)]),True,BLACK)
        numRect = numSurf.get_rect()
        numRect.topleft = (500,250)
        itemTexts[itemName] = [itemSurf,itemRect,numSurf,numRect]
# item surf;rect,number surf;rect
    isurf,irect,nsurf,nrect = itemTexts[itemNames[currentItem % len(itemNames)]] # change to current item name
    DISPLAYSURF.blit(isurf,irect)
    DISPLAYSURF.blit(nsurf,nrect)
    # event handling loop
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            x,y = event.pos
            #print str(x) + str(y)
            if pygame.Rect(x,y,1,1).colliderect(leftRect):
                do = -1
            elif pygame.Rect(x,y,1,1).colliderect(rightRect):
                do = -1
            elif pygame.Rect(x,y,1,1).colliderect(backButtonRect):
                back = True
            elif pygame.Rect(x,y,1,1).colliderect(sellButtonRect):
                sell = pack.keys()[currentItem % len(pack.keys())]
            elif pygame.Rect(x, y, 1, 1).colliderect(storeButtonRect):
                screen = 'store'
            elif pygame.Rect(x, y, 1, 1).colliderect(equipButtonRect):
                weapon = pack.keys()[currentItem % len(pack.keys())]
                print str(weapon)
        elif event.type == QUIT:
            save(name, apple, appleTree, costPerTree, startBlood, pack)
            pygame.quit()
            sys.exit()

    return (do,back,screen,weapon,sell)

def storeScreen(DISPLAYSURF, font, items, currentItem, apple): # TODO should I make packScreen() and storeScreen() together? They are too similar.
    DISPLAYSURF.fill(WHITE)
    currentItem %= len(items)
    do = 0  # switch the item
    back = False  # go back to home page?
    buy = None # buy anything?
    # draw 'Store' title
    titleSurf = font.render('Store', True, BLACK)
    titleRect = titleSurf.get_rect()
    titleRect.center = (400, 50)
    DISPLAYSURF.blit(titleSurf, titleRect)
    # draw arrows
    leftArrow = pygame.image.load('./left.png')
    leftRect = leftArrow.get_rect()
    leftRect.topleft = (100, 250)
    rightArrow = pygame.image.load('./right.png')
    rightRect = rightArrow.get_rect()
    rightRect.topleft = (600, 250)
    DISPLAYSURF.blit(leftArrow, (100, 250))
    DISPLAYSURF.blit(rightArrow, (600, 250))
    # back button
    backButtonRect = placeButton(DISPLAYSURF, font, 'back', 650, 500)
    # get item names
    itemNames = []
    for item in items:
        itemNames.append(item.name)
    # draw item name
    itemNameSurf = font.render(itemNames[currentItem],True,BLACK)
    itemNameRect = itemNameSurf.get_rect()
    itemNameRect.center = (400,300)
    DISPLAYSURF.blit(itemNameSurf,itemNameRect)
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONUP:
            x,y = event.pos
            rect = pygame.Rect(1,1,x,y)
            if rect.colliderect(leftRect):
                do = -1
            elif rect.colliderect(rightRect):
                do = 1
            elif rect.colliderect(backButtonRect):
                back = True
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


    return do,back,buy

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

    loadedPack = details[5]
    pack = eval(loadedPack)
    #serializedPack = details[5]
    #lstedPack = pickle.loads(serializedPack)
    #for item in stringedPack:
    #    stats = item.split(' ')
    #    if stats[0] == 'Material':
    #        if len(stats) < 5:
    #            stats.append(())
    #        addItem = Material(stats[1],bool(stats[2]),int(stats[3]),tuple(stats[4]))
    #    elif stats[0] == 'Food':
    #        if len(stats) < 6:
    #            stats.append(())
    #        addItem = Food(stats[1],int(stats[2]),bool(stats[3]),int(stats[4]),tuple(stats[5]))
    #    elif stats[0] == 'Weapon':
    #        addItem = Weapon(stats[1],int(stats[2]),int(stats[3]),tuple(stats[4]))
    #    pack.append(addItem)


    #       playername       apple       apple tree   apple cost per tree   start blood
    return details[0], int(details[1]), int(details[2]), int(details[3]), int(details[4]), pack


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
            save(name, apple, appleTree, costPerTree, startBlood, pack)
            pygame.quit()
            sys.exit()


def placeButton(surf, font, text, x, y):
    # draw sell button
    textButtonSurf = font.render(text, True, WHITE, NAVYBLUE)
    textButtonRect = textButtonSurf.get_rect()
    buttonRect = pygame.Rect(x, y, textButtonRect.width, textButtonRect.height)
    textButtonRect.topleft = (x, y)
    surf.blit(textButtonSurf, textButtonRect)
    return buttonRect


def save(name,apple,appleTree,costPerTree,blood,pack):
    name = name + '#usrname'
    apple = str(apple) + '#apple'
    appleTree = str(appleTree) + '#appleTree'
    costPerTree = str(costPerTree) + '#costPerTree'
    blood = str(blood) + '#blood'
    lstPack = []
    for item in pack.keys():
        if pack[item] == 1:
            lstPack.append(item)
        elif pack[item] > 1:
            for i in range(pack[item]):
                lstPack.append(item)
    #serializedLstPack = pickle.dumps(lstPack)
    #strPack = []
    #for item in pack:
    #    if isinstance(item,Food):
    #        if item.recipe == ():
    #            recipe = '()'
    #       else:
    #            recipe = str(item.recipe)
    #        itemStr = ' '.join(['Food',item.name,str(item.fullness),str(item.Craftable),str(item.cost),recipe])
    #    elif isinstance(item,Weapon):
    #        if item.recipe == ():
    #            recipe = '()'
    #        else:
    #            recipe = str(item.recipe)
    #        itemStr = ' '.join(['Weapon',item.name,str(item.harm),str(item.cost),recipe])
    #   elif isinstance(item,Material):
    #       if item.recipe == ():
    #            recipe = '()'
    #        else:
    #            recipe = str(item.recipe)
    #        itemStr = ' '.join(['Material',item.name,str(item.Craftable),str(item.cost),recipe])
    #    strPack.append(itemStr)
    packStr = lstPack
    statStr = '\n'.join((name,apple,appleTree,costPerTree,blood))
    finalStr = statStr + '\n\n' + packStr

    f = open('.\UsrStat.txt','w')
    f.write(finalStr)
    f.close()
    return

if __name__ == '__main__':
    main()
