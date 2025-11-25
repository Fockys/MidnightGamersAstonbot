import math

class playerClass():
    def __init__(self,stats,xp,skillPoints):
        self.discordUser = None
        self.xp = xp
        self.levelConst = 1
        self.skillPoints = skillPoints

        self.str = stats[0]
        self.dex = stats[1]
        self.con = stats[2]
        self.int = stats[3]
        self.wis = stats[4]
        self.cha = stats[5]


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
    

stats = (0,0,0,0,0,0)
xp = 500
player = playerClass(stats,xp)
print(player.getLevel())

