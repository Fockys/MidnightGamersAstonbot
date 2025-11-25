import math
from botMain import botClient
import os
import sys


class playerClass():
    def __init__(self,id,client:botClient):
        self.client = client
        self.id = id
        self.levelConst = 1
        self.getPlayer()

    def getPlayer(self):
        get = self.client.dbHan.getRPGUser(self.id)

        self.xp = get[1]
        self.skillPoints = get[9]

        self.str = get[2]
        self.dex = get[3]
        self.con = get[4]
        self.int = get[5]
        self.wis = get[6]
        self.cha = get[7]

        self.spell = get[10]
        self.hp = get[8]
        


    def changeStrength(self,amount):
        self.str += amount
    def changeDexterity(self,amount):
        self.dex += amount
    def changeConsitution(self,amount):
        self.con += amount
    def changeIntelligence(self,amount):
        self.int += amount
    def changeWisdom(self,amount):
        self.wis += amount
    def changeCharisma(self,amount):
        self.cha += amount

    def getStats(self):
        return(self.str,self.dex,self.con,self.int,self.wis,self.cha)
    
    def getLevel(self):
        return math.floor(self.levelConst*math.sqrt(self.xp))
    

