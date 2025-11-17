import discord
from discord import app_commands
from discord.ext import commands

class economyCog(commands.Cog):
    def __init__(self,client:commands.Bot):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("economy loaded")

    @app_commands.command(name="cash",description="get the amount of currency you have")
    async def getCurrency(self,interaction):
        await interaction.response.send_message("you have "+self.client.currencySymbol+str(self.client.dbHan.getCurrency(interaction.user.id)))

    @app_commands.command(name="leaderboard",description="Shows the 10 richest users")
    async def leaderBoard(self,interaction:discord.Interaction):
        top10 = self.client.dbHan.getTop10()
        des= ""
        print("test")
        for i in range(len(top10)):
            try:
                user= await self.client.fetch_user(top10[i][0])
                des = des + str(i)+" | "+str(user.name)+" : "+self.client.currencySymbol+str(top10[i][1])+"\n"
            except Exception as e:
                print(top10[i])
                print(e)
        embed = discord.Embed(
            title="Leaderboard",
            description= des
        )
        await interaction.response.send_message(embed=embed)
        

async def setup(client):
    await client.add_cog(economyCog(client))

    