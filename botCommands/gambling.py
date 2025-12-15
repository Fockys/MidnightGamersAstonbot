import discord
from discord import app_commands
from discord.ext import commands
import random
import math
from botMain import botClient
from botCommands.gamblingHelper.blackjack import blackjackGame
from botCommands.gamblingHelper.slots import slotsGame




#gambling cog
class gamblingCog(commands.Cog):
    def __init__(self,client:botClient):
        self.client = client
        self.blackjackGames  = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("gambling loaded")

    #50/50 coin flip, user loses currency on loss, wins currency on win 
    @app_commands.command(name="flip",description="Coin flip 50/50")
    @app_commands.describe(amount="Amount to bet")
    async def coinFlip(self,interaction:discord.Interaction, amount:str):

        if amount.isdigit() == False:
            await interaction.response.send_message("invalid amount")
            return
        amount = int(amount)

        user = self.client.dbHan.getUser(interaction.user.id)
        
         
        
        if user.Currency < amount:
            await interaction.response.send_message("lacking funds")
            return 0
        chance = random.random()
        if chance>0.5:
            self.client.dbHan.increaseCurrency(interaction.user.id,amount)
            des = "You won the flip"
            bal = str(user.Currency+amount)
        else:
            self.client.dbHan.increaseCurrency(interaction.user.id,-amount)
            des = "You lost the flip"
            bal = str(user.Currency-amount)

        embed = discord.Embed(
            title="Coin Flip",
            description= des
        )
        embed.add_field(name="Your Remaining balance is",
            value=self.client.currencySymbol+bal,
            inline=False)
        await interaction.response.send_message(embed=embed)



    #handles the buttons for the blackjack game
    class blackjackButtons(discord.ui.View):
        def __init__(self,outter,interaction:discord.Interaction,timeout=60):
            super().__init__(timeout=timeout)
            self.outter = outter
            self.interaction = interaction


        async def on_timeout(self):
            gameEmbed = discord.Embed(title="Blackjack")
            gameEmbed.add_field(name="Game Timed out ",value="You lost ")
            
            await self.interaction.edit_original_response(embed=gameEmbed,view=None)
            self.outter.blackJackEnd(self.interaction.user.id)
            return await super().on_timeout()
        
        
        #creates the button for hit and its behaviour
        @discord.ui.button(label="Hit",style=discord.ButtonStyle.gray)
        async def hitPressed(self,interaction:discord.Interaction,button:discord.Button):
            try:
                self.outter.blackjackGames[interaction.user.id].hitUser()
                gameEmbed = discord.Embed(title="Blackjack")
                gameEmbed.add_field(name="Dealer Hand",value=self.outter.blackjackGames[interaction.user.id].niceBotDeck(False),inline=False)
                gameEmbed.add_field(name=interaction.user.display_name+"'s hand",value=self.outter.blackjackGames[interaction.user.id].niceUserDeck(),inline=False)
                if self.outter.blackjackGames[interaction.user.id].isBustUser():
                    betAmount = self.outter.blackjackGames[interaction.user.id].bet
                    gameEmbed.set_field_at(0,name="Dealer Hand",value=self.outter.blackjackGames[interaction.user.id].niceBotDeck(True),inline=False)
                    gameEmbed.add_field(name="Game Over",value="You lost "+self.outter.client.currencySymbol+str(betAmount))
                    self.outter.blackJackEnd(interaction.user.id)
                    
                    await interaction.response.edit_message(embed=gameEmbed,view=None)
                else:
                    await interaction.response.edit_message(embed=gameEmbed)
            except Exception as e:
                print(e)

        

        #creates the button for stand and its behaviour
        @discord.ui.button(label="Stand",style=discord.ButtonStyle.gray)
        async def standPressed(self,interaction:discord.Interaction,button:discord.Button):
            try:
                result = self.outter.blackjackGames[interaction.user.id].userStay()
                gameEmbed = discord.Embed(title="Blackjack")
                gameEmbed.add_field(name="Dealer Hand",value=self.outter.blackjackGames[interaction.user.id].niceBotDeck(True),inline=False)
                gameEmbed.add_field(name=interaction.user.display_name+"'s hand",value=self.outter.blackjackGames[interaction.user.id].niceUserDeck(),inline=False)
                betAmount = self.outter.blackjackGames[interaction.user.id].bet
                #0 is a tie, 1 is a loss, 2 is win, 3 is win with bonus
                if result == 0:
                    gameEmbed.add_field(name="Game Over",value="Tie")
                    self.outter.client.dbHan.increaseCurrency(interaction.user.id,betAmount)
                elif result == 1:
                    gameEmbed.add_field(name="Game Over",value="You lost "+self.outter.client.currencySymbol+str(betAmount))
                elif result >= 2:
                    bonusMsg = ""
                    bonus = 0
                    if result==3:
                        bonus = math.ceil(betAmount*0.5)
                        bonusMsg = " + bonus " + self.outter.client.currencySymbol+str(bonus)
                    gameEmbed.add_field(name="Game Over",value="You won "+self.outter.client.currencySymbol+str(betAmount)+bonusMsg)
                    self.outter.client.dbHan.increaseCurrency(interaction.user.id,betAmount*2+bonus)
                self.outter.blackJackEnd(interaction.user.id)
            
                try:
                    gameEmbed.set_field_at(0,name="Dealer Hand",value=self.outter.blackjackGames[interaction.user.id].niceBotDeck(True),inline=False)
                except Exception as e:
                    print(e)
                await interaction.response.edit_message(embed=gameEmbed,view=None)
            except Exception as e:
                print(e)




    def blackJackEnd(self,id):
        del[self.blackjackGames[id]]

    @app_commands.command(name="endblackjack",description="force ends blackjack")
    @app_commands.describe(target="person to target")
    @app_commands.default_permissions()
    async def endBlackjack(self,interaction:discord.Interaction,target:discord.Member):
        self.blackJackEnd(target.id)
        await interaction.response.send_message("Game stopped for target",ephemeral=True)



    #blackjack
    @app_commands.command(name="blackjack",description="starts blackjack game")
    @app_commands.describe(amount="Amount to bet")
    async def blackjack(self,interaction:discord.Interaction,amount:str):
        #ensures bet amount is valid
        if amount.isdigit() == False:
            await interaction.response.send_message("invalid amount")
            return 0
        user = self.client.dbHan.getUser(interaction.user.id)
        if user.Currency < int(amount):
            await interaction.response.send_message("lacking funds")
            return 0
        #checks if the user is in a game or not already, 1 game per user playing
        if interaction.user.id in self.blackjackGames:
            failEmbed = discord.Embed(title="Blackjack error",description="You are already in a game")
            await interaction.response.send_message(embed=failEmbed)
            return
        #takes user money
        self.client.dbHan.increaseCurrency(interaction.user.id,-(int(amount)))
        #creates blackjack game and setsup
        self.blackjackGames[interaction.user.id] = blackjackGame(int(amount))
        gameEmbed = discord.Embed(title="Blackjack")
        
        gameEmbed.add_field(name="Dealer Hand",value=self.blackjackGames[interaction.user.id].niceBotDeck(False),inline=False)
        gameEmbed.add_field(name=interaction.user.display_name+"'s hand",value=self.blackjackGames[interaction.user.id].niceUserDeck(),inline=False)


        await interaction.response.send_message(embed=gameEmbed,view = self.blackjackButtons(self,interaction))


    #slots fruits
    @app_commands.command(name="slots",description="starts slots game")
    @app_commands.describe(amount="Amount to bet")
    async def slots(self,interaction:discord.Interaction,amount:str):
        #ensures bet amount is valid
        if amount.isdigit() == False:
            await interaction.response.send_message("invalid amount")
            return
        if int(amount) > 1000:
            await interaction.response.send_message("Max bet is set at 1000")
            return
        if int(amount)<3:
            await interaction.response.send_message("Min bet set at 3")
            return
        user = self.client.dbHan.getUser(interaction.user.id)
        if user.Currency < int(amount):
            await interaction.response.send_message("lacking funds")
            return
        
        amount = int(amount)
        
        #deducts bet amount from user
        self.client.dbHan.increaseCurrency(interaction.user.id,-amount)

        #starts a slot game
        result = slotsGame()

        #outputs and sets correct prize
        jackpot = self.client.dbHan.getJackpot()
        if result[0] == 100:
            prize = jackpot
            pass #jackpot behaviour
        else:
            prize = result[0]*amount
        try:
            gameEmbed = discord.Embed(title = "slots",description=result[1])
            if prize == 0:
                gameEmbed.add_field(name="You lost",value=str(amount))
                amount = math.floor(amount*0.9)
                self.client.dbHan.setJackpot(jackpot+amount)
            else:
                gameEmbed.add_field(name="you won",value=prize)
            
            gameEmbed.add_field(name="current jackpot",value=jackpot+amount)
            self.client.dbHan.increaseCurrency(interaction.user.id,prize)
            await interaction.response.send_message(embed=gameEmbed)
        except Exception as e:
            print("problem in response")
            print(e)
        return


        
    
    

    

async def setup(client):
    await client.add_cog(gamblingCog(client))


