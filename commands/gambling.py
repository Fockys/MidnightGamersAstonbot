import discord
from discord import app_commands
from discord.ext import commands
import random

#gambling cog
class gamblingCog(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("gambling loaded")

    #50/50 coin flip, user loses currency on loss, wins currency on win 
    @app_commands.command(name="flip",description="Coin flip 50/50")
    @app_commands.describe(amount="Amount to bet")
    async def coinFlip(self,interaction, amount:str):

        if amount.isdigit() == False:
            await interaction.response.send_message("invalid amount")
            return 0
        
        amount = int(amount)
        user = self.client.dbHan.getUser(interaction.user.id)
        print(user)
        user=user[0]
         
        chance = random.random()
        if user[1] < amount:
            await interaction.response.send_message("lacking funds")
            return 0
        if chance>0.5:
            self.client.dbHan.increaseCurrency(interaction.user.id,amount)
            des = "You won the flip"
            bal = str(user[1]+amount)
        else:
            self.client.dbHan.increaseCurrency(interaction.user.id,-amount)
            des = "You lost the flip"
            bal = str(user[1]+amount)

        embed = discord.Embed(
            title="Coin Flip",
            description= des
        )
        embed.add_field(name="Your Remaining balance is",
            value=self.client.currencySymbol+bal,
            inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(gamblingCog(client))


