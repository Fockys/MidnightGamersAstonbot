import discord
from discord import app_commands
from discord.ext import commands

class generalCog(commands.Cog):
    def __init__(self,client:commands.Bot):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("general loaded")

    @app_commands.command(name="profile",description="Shows a user profile")
    async def profile(self,interaction:discord.Interaction):
        try:
            user = interaction.user
            userDb = self.client.dbHan.getUser(user.id)[0]

            embed=discord.Embed(title=user.display_name,description=user.top_role)
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.add_field(name="Joined",value=str(user.joined_at.date()))
            embed.add_field(name="Currency",value=str(userDb[1])+self.client.currencySymbol)


            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)



async def setup(client):
    await client.add_cog(generalCog(client))