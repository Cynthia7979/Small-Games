import pygame, random
from pygame.locals import *

costPerTree = 0
class Item(object):
    def __init__(self,itemName,isTool,isFood,isWeapon,isCraftable,cost):
        self.name = str(itemName)
        self.isTool = isTool
        self.isFood = isFood
        self.isWeapon = isWeapon
        self.Craftable = isCraftable
        self.cost = cost


class Weapon(Item):
    def __init__(self,itemName,harm,cost):
        super(Weapon,self).__init__(itemName,False,False,True,True,cost) # all weapons are craftable
        self.harm = harm


class Food(Item):
    def __init__(self,itemName,fullness,craftable,cost,isPotion=False,potionType=None,useDegree=None):
        super(Food,self).__init__(itemName,False,True,False,craftable,cost)
        self.fullness = fullness
        self.isPotion = isPotion
        self.type = potionType
        self.degree = useDegree

class mob(object):
    def __init__(self,blood,damage,trophies):
        self.blood = blood
        self.damage = damage
        self.trophie = trophies

#class Tool(Item):
#    def __init__(self,):
# Coming "soon"!!

def pickApple(appleTree):
    tuple = (False,False,True)
    doExtra = random.choice(tuple)
    if doExtra:
        applePerTree = 5
    else:
        applePerTree = 3
    return appleTree * applePerTree

def buyJustice(money,thing):
    if thing.cost > money:
        return False
    else:
        return True

def plantTreeJustice(num,apple):
    if num*costPerTree < apple:
        return True
    else:
        return False
a = Weapon('a',3,13)
