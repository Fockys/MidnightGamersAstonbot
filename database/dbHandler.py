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
                CREATE TABLE users (
                    USERID BIGINT PRIMARY KEY NOT NULL,
                    CURRENCY INTEGER NOT NULL,
                    LASTCOIN INTEGER,
                    LASTSTEAL INTEGER

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



if __name__ == "__main__":
    dbHan = handler()
    dbHan.createTable()




