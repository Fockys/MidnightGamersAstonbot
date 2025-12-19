import discord
from discord import app_commands
from discord.ext import commands
import time
import random
from botMain import botClient
import math
import datetime

MemberRole = 1445207809649021030 

class economyCog(commands.Cog):
    def __init__(self,client:botClient):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("economy loaded")

    @app_commands.command(name="cash",description="get the amount of currency you have")
    async def getCurrency(self,interaction):
        try:
            user = self.client.dbHan.getUser(interaction.user.id)
            await interaction.response.send_message("you have "+self.client.currencySymbol+str(user.Currency))
        except Exception as e:
            print("/cash failure")
            print(e)

    @app_commands.command(name="topcurrency",description="Shows the 10 richest users")
    async def leaderBoard(self,interaction:discord.Interaction):
        numberEmojis = {1:"1️⃣",2:"2️⃣",3:"3️⃣",4:"4️⃣",5:"5️⃣",6:"6️⃣",7:"7️⃣",8:"8️⃣",9:"9️⃣",10:"🔟"}
        top10 = self.client.dbHan.getTop10()
        des= ""
        for i in range(len(top10)):
            try:
                user= await self.client.fetch_user(top10[i][0])
                des = des + numberEmojis[i+1]+" | <@"+str(user.id)+"> | "+self.client.currencySymbol+str(top10[i][1])+"\n"
            except Exception as e:
                print(top10[i])
                print(e)
        embed = discord.Embed(
            title="Top richest users",
            description= des
        )
        await interaction.response.send_message(embed=embed)
        

    @app_commands.command(name="steal",description="steal from someone, chance to get caught")
    @app_commands.describe(target="person to target")
    async def steal(self,interaction:discord.Interaction,target:discord.Member):

        

        if interaction.user.id == target.id:
            await interaction.response.send_message("You cant steal from yourself")
            return

        userDB = self.client.dbHan.getUser(interaction.user.id)
        targetDB = self.client.dbHan.getUser(target.id)
        try:
            currentTime = time.time()
            if userDB.lastSteal==None or currentTime>userDB.lastSteal+900:
                success = random.random()
                if success > 0.8:
                    lost = math.ceil(userDB.Currency)
                    await interaction.response.send_message("You got caught and lost it all")
                    self.client.dbHan.increaseCurrency(interaction.user.id,-lost)
                else:
                    
                    stealAmount = math.ceil(targetDB.Currency*0.01)
                    

                    await interaction.response.send_message("You succesffuly stole "+self.client.currencySymbol + str(stealAmount) + " from "+target.name)
                    self.client.dbHan.increaseCurrency(interaction.user.id,stealAmount)
                    self.client.dbHan.increaseCurrency(target.id,-stealAmount)
                self.client.dbHan.writeLastSteal(interaction.user.id)
            else:
                await interaction.response.send_message("Command has a 15 minute cooldown per person")
        except Exception as e:
            print(e)

    @app_commands.command(name="give",description="give money to someone")
    @app_commands.describe(target="person to target",amount="amount of money to give")
    async def give(self,interaction:discord.Interaction,target:discord.Member,amount:app_commands.Range[int,1,100000]):
        amount = str(amount)
        if interaction.user.id == target.id:
            await interaction.response.send_message("You cant give to yourself")
            return
        try:
            #ensures give amount is valid
            if amount.isdigit() == False:
                await interaction.response.send_message("invalid amount")
                return
            user = self.client.dbHan.getUser(interaction.user.id)
            amount = int(amount)
            if user.Currency < amount:
                await interaction.response.send_message("lacking funds")
                return
            
            #takes money from interaction author and gives to the target
            self.client.dbHan.increaseCurrency(target.id,amount)
            self.client.dbHan.increaseCurrency(interaction.user.id,-amount)
            await interaction.response.send_message("Gave "+str(amount)+self.client.currencySymbol+" to "+target.name)
        except Exception as e:
            print(e)

"""
This command was such a bad idea
    @app_commands.command(name="buytimeout",description="time out someone for 1 minute, cost is 1000 coins")
    @app_commands.describe(target="person to target")
    async def buyTimeOut(self,interaction:discord.Interaction,target:discord.User):
        if interaction.guild.get_role(MemberRole) not in interaction.user.roles:
            await interaction.response.send_message("Only members can use this command")
            return
        user = self.client.dbHan.getUser(interaction.user.id)
        if user.Currency < 1000:
            await interaction.response.send_message("lacking funds, this costs 1000 coins")
            return
        
        self.client.dbHan.increaseCurrency(interaction.user.id,-200)
        await interaction.guild.get_member(target.id).timeout(datetime.timedelta(seconds=60))
        await interaction.response.send_message(target.mention+" timed out for 1 min")
"""

async def setup(client):
    await client.add_cog(economyCog(client))

    