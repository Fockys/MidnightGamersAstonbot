import discord
from discord import app_commands
from discord.ext import commands
from botMain import botClient

class generalCog(commands.Cog):
    def __init__(self,client:botClient):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("general loaded")

    @app_commands.command(name="profile",description="Shows a user profile")
    async def profile(self,interaction:discord.Interaction):
        try:
            user = interaction.user
            userDb = self.client.dbHan.getUser(user.id)

            embed=discord.Embed(title=user.display_name,description=user.top_role)
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.add_field(name="Joined",value=str(user.joined_at.date()))
            embed.add_field(name="Currency",value=str(userDb.Currency)+self.client.currencySymbol)


            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)


    @app_commands.command(name="topactivity",description="Shows the 10 most active users")
    async def leaderBoardActibity(self,interaction:discord.Interaction):
        numberEmojis = {1:"1️⃣",2:"2️⃣",3:"3️⃣",4:"4️⃣",5:"5️⃣",6:"6️⃣",7:"7️⃣",8:"8️⃣",9:"9️⃣",10:"🔟"}
        top10 = self.client.dbHan.getTop10Activity()
        des= ""
        for i in range(len(top10)):
            try:
                user= await self.client.fetch_user(top10[i][0])
                des = des + numberEmojis[i+1]+" | "+str(user.name)+" | "+str(top10[i][4])+"\n"
            except Exception as e:
                print(top10[i])
                print(e)
        embed = discord.Embed(
            title="Top active users",
            description= des
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="credits",description="credits to people who helped with ths bot")
    async def credits(self,interaction:discord.Interaction):
        await interaction.response.send_message(content="Thanks to @inf1nitea for blackjack aces fix")


async def setup(client):
    await client.add_cog(generalCog(client))