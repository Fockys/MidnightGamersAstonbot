import psycopg2
import os
import time
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
                CREATE TABLE IF NOT EXISTS slots (
                  USERID BIGINT PRIMARY KEY NOT NULL,
                  JACKPOT INTEGER NOT NULL
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
                INSERT INTO users (USERID,CURRENCY,XP) VALUES (%i,0,0)"""%(id))


    #returns -1 for no user
    def getUser(self,id):
        self.c.execute("SELECT * FROM users WHERE USERID=%i"%(id))
        result = self.c.fetchall()
        if result == []:
            self.newUser(id)
            self.c.execute("SELECT * FROM users WHERE USERID=%i"%(id))
            result = self.c.fetchall()
        return result

    #-1 returns means user doesnt exist
    def getXP(self,id):
        return(self.getUser(id)[0][2])
    
    def getCurrency(self,id):
        return(self.getUser(id)[0][1])

    def increaseXP(self,id,increase):
        user = self.getUser(id)
        if user == -1:
            self.newUser(id)
            user = self.getUser(id)
        self.c.execute("UPDATE users SET XP=%i WHERE USERID = %i"%(user[0][2]+increase,id))
        self.commit()

    def increaseCurrency(self,id,increase):
        user = self.getUser(id)
        if user == -1:
            self.newUser(id)
            user = self.getUser(id)
        self.c.execute("UPDATE users SET CURRENCY=%i WHERE USERID = %i"%(user[0][1]+increase,id))
        self.commit()

    def writeLastCoinNow(self,id):
        user = self.getUser(id)
        if user == -1:
            self.newUser(id)
            user = self.getUser(id)
        currentTime = time.time()
        self.c.execute("UPDATE users SET Lastcoin =%i WHERE USERID = %i"%(currentTime,id))

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
        except:
            print("failed to set jackpot")

if __name__ == "__main__":
    dbHan = handler()




