import discord
from discord.ext import commands
import database.dbHandler as db
import asyncio
import os
import datetime
import time

#bot token
try:
    TOKEN= os.environ['TOKEN']
    
except:


    print("Environment token not found")
    
   

#The bot class itself
class botClient(commands.Bot):
    _watcher: asyncio.Task

    def __init__(self):
        #gets the database handler
        self.dbHan = db.handler()
        #the symbol to be used with currency
        self.currencySymbol = "🪙"
        

        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )

    #on setup get all the different extensions found under commands and load them
    async def setup_hook(self):
        for filename in os.listdir("./botCommands"):
            if filename.endswith("py"):
                await client.load_extension(f"botCommands.{filename[:-3]}")
        await client.load_extension(f"miniAstonRpg.rpgCommands")
        await sync()



client = botClient()

#sync slash commands with discord
async def sync():
    print("Starting sync")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except:
        print("Sync failed")

#when client is ready print message
@client.event
async def on_ready():
    print("logged in as:",client.user.name)
    
    try:
        server = client.guilds[0]
        print("currently in : " + server.name)
        for channel in server.channels:
            if channel.name == "logs":
                client.logChannel = channel
                
    except Exception as e:
        print(e)
    

 
@client.event
async def on_message(message:discord.Message):
    if message.author != client.user:
        #logging
        nowTime = str(datetime.datetime.now().strftime("%H:%M:%S"))
        await client.logChannel.send(nowTime+" | "+message.author.name+ " in " + message.channel.name + " : "+ message.content.replace("<","").replace(">",""))

        user = client.dbHan.getUser(message.author.id)

        #checks if user is eligbile for next coin
        if user.lastCoin == None or (time.time()>user.lastCoin+60):
            #increases currency by 1 or 2 for message author depending on if they are a member
            if "1445207809649021030" in [y.id for y in message.author.roles]:
                client.dbHan.increaseCurrency(message.author.id,2)
            
            else:
                client.dbHan.increaseCurrency(message.author.id,1)
            client.dbHan.writeLastCoinNow(message.author.id)

#start bot
async def main():
    async with client:
        await client.start(TOKEN)


if __name__ == "__main__":
    #start main
    asyncio.run(main())



