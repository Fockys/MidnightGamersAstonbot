import discord
from discord import app_commands
from discord.ext import commands
from botMain import botClient


class rpgCog(commands.Cog):
    def __init__(self,client:botClient):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("rpgCommands loaded")




async def setup(client):
    await client.add_cog(rpgCog(client))