import discord
from discord.ext import commands
import database.dbHandler as db
import asyncio
import os

#bot token
TOKEN = None

#The bot class itself
class botClient(commands.Bot):
    _watcher: asyncio.Task

    def __init__(self):
        #gets the database handler
        self.dbHan = db.handler("db.db")
        #the symbol to be used with currency
        self.currencySymbol = "🪙"

        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )

    #on setup get all the different extensions found under commands and load them
    async def setup_hook(self):
        for filename in os.listdir("./commands"):
            if filename.endswith("py"):
                await client.load_extension(f"commands.{filename[:-3]}")
        await sync()

client = botClient()

#sync slash commands with discord
async def sync():
    print("Starting sync")
    try:
        guild = discord.Object(id=1383922325065564210)
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except:
        print("Sync failed")

#when client is ready print message
@client.event
async def on_ready():
    print("logged in as:",client.user.name)
 
@client.event
async def on_message(message):
    if message.author != client.user:
        #prints chat to command line
        print(message.author.name + ":" +message.content)
        #icreases currency by 1 for message author
        client.dbHan.increaseCurrency(message.author.id,1)

#start bot
async def main():
    async with client:
        await client.start(TOKEN)

#start main
asyncio.run(main())



