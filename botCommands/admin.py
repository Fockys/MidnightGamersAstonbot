import discord
from discord import app_commands
from discord.ext import commands
from botMain import botClient
ownerID = 459034429956947968

class adminCog(commands.Cog):
    def __init__(self,client:botClient):
        self.client = client


    @app_commands.command(name="admingive",description="give money to someone")
    @app_commands.describe(target="person to target",amount="amount of money to give")
    @app_commands.default_permissions()
    async def admingive(self,interaction:discord.Interaction,target:discord.Member,amount:str):
        if interaction.user.id != ownerID:
            await interaction.response.send_message("not authorized")
            return
        try:
            #ensures give amount is valid
            if amount.isdigit() == False:
                await interaction.response.send_message("invalid amount")
                return
            user = self.client.dbHan.getUser(interaction.user.id)
            amount = int(amount)
            #takes money from interaction author and gives to the target
            self.client.dbHan.increaseCurrency(target.id,amount)
            await interaction.response.send_message("Gave "+str(amount)+self.client.currencySymbol+" to "+target.name,ephemeral=True)
        except Exception as e:
            print(e)


    @app_commands.command(name="admintake",description="give money to someone")
    @app_commands.describe(target="person to target",amount="amount of money to give")
    @app_commands.default_permissions()
    async def admintake(self,interaction:discord.Interaction,target:discord.Member,amount:str):
        if interaction.user.id != ownerID:
            await interaction.response.send_message("not authorized")
            return
        try:
            #ensures give amount is valid
            if amount.isdigit() == False:
                await interaction.response.send_message("invalid amount")
                return
            user = self.client.dbHan.getUser(interaction.user.id)
            amount = int(amount)
            #takes money from interaction author and gives to the target
            self.client.dbHan.increaseCurrency(target.id,-amount)
            await interaction.response.send_message("took "+str(amount)+self.client.currencySymbol+" from "+target.name,ephemeral=True)
        except Exception as e:
            print(e)



        







async def setup(client):
    await client.add_cog(adminCog(client))