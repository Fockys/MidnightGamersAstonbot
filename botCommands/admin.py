import discord
from discord import app_commands
from discord.ext import commands
from botMain import botClient

ownerID = 459034429956947968
studentRole = 1437269465950584893 
MemberRole = 1445207809649021030 
externalRole = 1442508308551434312

class adminCog(commands.Cog):
    def __init__(self,client:botClient):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("admin loaded")


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


    @app_commands.command(name="getastonid",description="Get aston id froma discord ping")
    @app_commands.describe(target="The persons ID to get")
    @app_commands.default_permissions(kick_members=True)
    async def getAstonID(self,interaction:discord.Interaction, target:discord.Member):
        user = self.client.dbHan.getStudentFromDisc(interaction.user.id)
        if user[2] == False:
            await interaction.response.send_message("invalid permissions",ephemeral=True)
            return
        target = self.client.dbHan.getStudentFromDisc(target.id)
        if target == -1:
            await interaction.response.send_message("Target is not a student or not in DB")
            return
        await interaction.response.send_message("<@"+str(target[0])+"> | astonID = "+str(target[1])+" | isMember = "+str(target[3]),ephemeral=True)

        
    @app_commands.command(name="setcommittee",description="sets target as committee member")
    @app_commands.describe(target="Aston ID of person to set")
    @app_commands.default_permissions()
    async def setCommittee(self,interaction:discord.Interaction,target:int):
        
        if interaction.user.id != ownerID:
            await interaction.response.send_message("invalid permissions",ephemeral=True)
            return
        try:
            self.client.dbHan.setCommittee(target)
            await interaction.response.send_message(str(target)+" set as committee",ephemeral=True)
        except Exception as e:
            print(e)


    @app_commands.command(name="setmember",description="sets target as committee member")
    @app_commands.describe(target="Aston ID of person to set")
    @app_commands.default_permissions()
    async def setMember(self,interaction:discord.Interaction,target:int):
        
        user = self.client.dbHan.getStudentFromDisc(interaction.user.id)
        if user[2] == False:
            await interaction.response.send_message("invalid permissions",ephemeral=True)
            return
        
        role = interaction.guild.get_role(MemberRole)
        try:
            targetDiscID = self.client.dbHan.getStudentFromAstonID(target)[0]
            print(targetDiscID)
            targetMem = interaction.guild.get_member(targetDiscID)
            await targetMem.add_roles(role)
        except Exception as e:
            print("could not add role")
            print(e)


        try:
            self.client.dbHan.setMember(target)
            await interaction.response.send_message(str(target)+" set as member",ephemeral=True)
        except Exception as e:
            print(e)



    @app_commands.command(name="as",description="Add student to DB and give roles automatically")
    @app_commands.describe(target="The person to add",astonid="the persons aston ID")
    @app_commands.default_permissions()
    async def addStudent(self,interaction:discord.Interaction,target:discord.Member,astonid:int):

        user = self.client.dbHan.getStudentFromDisc(interaction.user.id)
        if user[2] == False:
            await interaction.response.send_message("invalid permissions",ephemeral=True)
            return
        
        t = self.client.dbHan.addStudent(target.id,astonid)
        if t == -1:
            await interaction.response.send_message("Target is already a student",ephemeral=True)
            return
        role = interaction.guild.get_role(studentRole)
        try:
            await target.add_roles(role)
        except Exception as e:
            print("could not add role")
            print(e)
        await interaction.response.send_message("<@"+str(target.id)+"> with astonID "+str(astonid)+" set as student",ephemeral=True)


    @app_commands.command(name="ae",description="Add external roles")
    @app_commands.describe(target="person to set as external")
    @app_commands.default_permissions(kick_members=True)
    async def addExternal(self,interaction:discord.Interaction,target:discord.Member):
        user = self.client.dbHan.getStudentFromDisc(interaction.user.id)
        if user[2] == False:
            await interaction.response.send_message("invalid permissions",ephemeral=True)
            return
        
        role = interaction.guild.get_role(externalRole)
        try:
            await target.add_roles(role)
        except:
            print("could not set role")
        await interaction.response.send_message("<@"+str(target.id)+"> set as external",ephemeral=True)

  







async def setup(client):
    await client.add_cog(adminCog(client))