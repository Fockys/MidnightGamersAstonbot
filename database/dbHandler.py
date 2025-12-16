import psycopg2
import os
import time

class userRecord():
    def __init__(self,userReturn):
        self.userId = userReturn[0]
        self.Currency = userReturn[1]
        self.lastCoin = userReturn[2]
        self.lastSteal = userReturn[3]

#handles the db with serveral functions to interact with it
class handler():
    def __init__(self):
        try:
            self.con = psycopg2.connect(os.environ['DATABASE_URL'],sslmode='require')
            
        except:
            print("environmental db variables not found")

        try:
            self.con.autocommit = True
            self.c = self.con.cursor()
            print("Successfully connected to db")
        except Exception as e:
            print(e)
            print("Failed to connect to db")


    def createTable(self):
        self.c.execute("""
                CREATE TABLE members (
                    USERID BIGINT PRIMARY KEY NOT NULL,
                    ASTONID INTEGER NOT NULL,
                    isMember BOOL,
                    isCommittee BOOL

                  )
                  """)

    def getTop10(self):
        self.c.execute("SELECT * FROM users ORDER BY currency DESC LIMIT 10")
        result = self.c.fetchall()
        return result

    def close(self):
        self.con.close()

    def newUser(self,id):
        self.c.execute("""
                INSERT INTO users (USERID,CURRENCY) VALUES (%i,0)"""%(id))
        
    def getUser(self,id):
        self.c.execute("SELECT * FROM users WHERE USERID=%i"%(id))
        result = self.c.fetchall()
        if result == []:
            self.newUser(id)
            self.c.execute("SELECT * FROM users WHERE USERID=%i"%(id))
            result = self.c.fetchall()
        return userRecord(result[0])


    def increaseXP(self,id,increase):
        user = self.getUser(id)
        if user == -1:
            self.newUser(id)
            user = self.getUser(id)
        self.c.execute("UPDATE users SET XP=%i WHERE USERID = %i"%(user[0][2]+increase,id))
        self.commit()

    def increaseCurrency(self,id,increase):
        user = self.getUser(id)
        self.c.execute("UPDATE users SET CURRENCY=%i WHERE USERID = %i"%(user.Currency+increase,id))
        self.commit()

    def writeLastCoinNow(self,id):
        user = self.getUser(id)
        if user == -1:
            self.newUser(id)
            user = self.getUser(id)
        currentTime = time.time()
        self.c.execute("UPDATE users SET Lastcoin =%i WHERE USERID = %i"%(currentTime,id))
        self.commit()

    def commit(self):
        self.con.commit()

    def writeLastSteal(self,id):
        user = self.getUser(id)
        if user == -1:
            self.newUser(id)
            user = self.getUser(id)
        currentTime = time.time()
        self.c.execute("UPDATE users SET Laststeal =%i WHERE USERID = %i"%(currentTime,id))


    def getJackpot(self):
        self.c.execute("SELECT * FROM slots")
        result = self.c.fetchone()[1]
        return(result)

    def setJackpot(self,jackpot):
        try:
            self.c.execute("UPDATE slots SET JACKPOT=%i WHERE USERID = 0"%(jackpot))
            self.commit()
        except:
            print("failed to set jackpot")

    def dropRPG(self):
        self.c.execute("DROP TABLE rpgusers")


    #rpg related command stuff

    def newRPGUser(self,id):
        self.c.execute("INSERT INTO rpgusers (userID,xp,skillpoints,hp,str,dex,con,int,wis,cha,lastHeal) VALUES (%i,0,0,0,0,0,0,0,0,0,0)"%(id))
    def getRPGUser(self,id):
        self.c.execute("SELECT * FROM rpgusers WHERE USERID = %i"%(id))
        result = self.c.fetchone()
        if result == None:
            self.newRPGUser(id)
            self.c.execute("SELECT * FROM slots WHERE USERID = %i"%(id))
            result = self.c.fetchone()
        return result
    
    #stuff for storing mappings of discord ids to aston ids
    def addStudent(self,discordID:int,astonID:int):
        self.c.execute("SELECT*FROM members WHERE userid = %i"%(discordID))
        result = self.c.fetchone()
        if result != None:
            return -1
        self.c.execute("INSERT INTO members (userid,astonid,iscommittee,ismember) VALUES (%i,%i,FALSE,FALSE)"%(discordID,astonID))
        self.commit()
        return 1

    #get a students id from there discord
    def getStudentFromDisc(self,discordID:int):
        self.c.execute("SELECT*FROM members WHERE userid = %i"%(discordID))
        result = self.c.fetchone()
        if result == None:
            return -1
        else:
            return result
        
    def getStudentFromAstonID(self,astonID:int):
        self.c.execute("SELECT*FROM members WHERE astonid = %i"%(astonID))
        result = self.c.fetchone()
        if result == None:
            return -1
        else:
            return result
        

    def setMember(self,astonID:int):
        self.c.execute("UPDATE members SET ismember = TRUE WHERE astonid=%i"%(astonID))
        self.commit()

    def setCommittee(self,astonID:int):
        self.c.execute("UPDATE members SET iscommittee = TRUE WHERE astonid=%i"%(astonID))

if __name__ == "__main__":
    dbHan = handler()
    s = dbHan.getStudentFromDisc(459034429956947968)
    print(s)





