import discord
from discord import app_commands
from discord.ext import commands

class economyCog(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("economy loaded")

    @app_commands.command(name="cash",description="get the amount of currency you have")
    async def getCurrency(self,interaction):
        await interaction.response.send_message("you have "+self.client.currencySymbol+str(self.client.dbHan.getCurrency(interaction.user.id)))

async def setup(client):
    await client.add_cog(economyCog(client))

    