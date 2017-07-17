import pygame, random
from pygame.locals import *

costPerTree = 0


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
    def __init__(self, itemName, fullness, craftable, cost, isPotion=False, potionType=None, useDegree=None):
        super(Food,self).__init__(itemName, False, True, False, craftable, cost)
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

# materials
wood = Material('wood', False, 3)
stick = Material('stick', True, 1, (wood,))
rock = Material('rock', False, 2)
copper = Material('copper ingot', True, 5, (rock, rock))
iron = Material('iron ingot', True, 12, (copper, copper, copper))
gold = Material('gold ingot', True, 27, (iron, iron, iron, iron))
diamond = Material('diamond!', True, 58, (gold, gold, gold, gold, gold))
# foods
flesh = Food('flesh', 2, False, 2)
# mobs
zombie = Mob('zombie', 20, 1, (flesh,))
tree = Mob('tree', 10, 0.5, (wood, stick))
stone = Mob('stone', 30, 0.5, (rock,))
# weapons
wooden_sword = Weapon('wooden sword', 2, 5, (wood, wood, stick))
stone_sword = Weapon('stone sword', 6, 12, (rock, rock, stick))
iron_sword = Weapon('iron sword', 18, 26, (iron, iron, stick))
golden_sword = Weapon('golden sword', 54, 54, (gold, gold, stick))
diamond_sword = Weapon('diamond sword', 162, 110, (diamond, diamond, stick))
better_wooden_sword = Weapon('better wooden sword', 10, 10, (wooden_sword, wooden_sword))  # and so on...

placeToMobs = {'forest':(tree,tree,tree,tree,tree)}