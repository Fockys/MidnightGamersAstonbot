import discord
from discord import app_commands
from discord.ext import commands
from miniAstonRpg.player import playerClass
from botMain import botClient


class rpgCog(commands.Cog):
    def __init__(self,client:botClient):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("rpgCommands loaded")


    @app_commands.command(name="rpgp",description="your rpg profile")
    async def rpgProfile(self,interaction:discord.Interaction):
        player = playerClass(interaction.user.id,self.client)
        try:
            embed=discord.Embed(title=interaction.user.display_name,description="Level "+str(player.getLevel())+"  | RPG WIP rn </3")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            if player.skillPoints>0:
                embed.add_field(name="Avaliable skillpoints",value=str(player.skillPoints),inline=False)
            embed.add_field(name="HP",value=str(player.hp))
            embed.add_field(name="Currency",value=str(self.client.dbHan.getUser(interaction.user.id).Currency)+self.client.currencySymbol)
            embed.add_field(name="Strength",value=str(player.str))
            embed.add_field(name="Speed",value=str(player.dex))
            embed.add_field(name="Defence", value=str(player.con))
            embed.add_field(name="Intelligence", value=str(player.int))
            embed.add_field
    



            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
        pass




async def setup(client):
    await client.add_cog(rpgCog(client))