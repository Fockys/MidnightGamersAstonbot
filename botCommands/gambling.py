import discord
from discord import app_commands
from discord.ext import commands
import random
import math
from botCommands.helper.blackjack import blackjackGame




#gambling cog
class gamblingCog(commands.Cog):
    def __init__(self,client):
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
            return 0
        amount = int(amount)

        user = self.client.dbHan.getUser(interaction.user.id)
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
            bal = str(user[1]-amount)

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
        def __init__(self,outter,timeout=30):
            super().__init__(timeout=timeout)
            self.outter = outter

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
                if result == 0:
                    gameEmbed.add_field(name="Game Over",value="Tie")
                elif result == 1:
                    gameEmbed.add_field(name="Game Over",value="You lost "+self.outter.client.currencySymbol+str(betAmount))
                elif result  == 2:
                    
                    gameEmbed.add_field(name="Game Over",value="You won "+self.outter.client.currencySymbol+str(betAmount))
                    self.outter.client.dbHan.increaseCurrency(interaction.user.id,betAmount*2)
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



    #blackjack
    @app_commands.command(name="blackjack",description="starts blackjack game")
    @app_commands.describe(amount="Amount to bet")
    async def blackjack(self,interaction:discord.Interaction,amount:str):
        #ensures bet amount is valid
        if amount.isdigit() == False:
            await interaction.response.send_message("invalid amount")
            return 0
        user = self.client.dbHan.getUser(interaction.user.id)
        user=user[0]
        if user[1] < int(amount):
            await interaction.response.send_message("lacking funds")
            return 0
        self.client.dbHan.increaseCurrency(interaction.user.id,-(int(amount)))
        #checks if the user is in a game or not already, 1 game per user playing
        if interaction.user.id in self.blackjackGames:
            failEmbed = discord.Embed(title="Blackjack error",description="You are already in a game")
            await interaction.response.send_message(embed=failEmbed)
            return
        #creates blackjack game and setsup
        self.blackjackGames[interaction.user.id] = blackjackGame(int(amount))
        gameEmbed = discord.Embed(title="Blackjack")
        
        gameEmbed.add_field(name="Dealer Hand",value=self.blackjackGames[interaction.user.id].niceBotDeck(False),inline=False)
        gameEmbed.add_field(name=interaction.user.display_name+"'s hand",value=self.blackjackGames[interaction.user.id].niceUserDeck(),inline=False)


        await interaction.response.send_message(embed=gameEmbed,view = self.blackjackButtons(self))


    #slots fruits
    @app_commands.command(name="slots",description="starts slots game")
    @app_commands.describe(amount="Amount to bet")
    async def slots(self,interaction:discord.Interaction,amount:str):
        #ensures bet amount is valid
        if amount.isdigit() == False:
            await interaction.response.send_message("invalid amount")
            return 0
        if int(amount) > 100:
            await interaction.response.send_message("Max bet is set at 100")
        if int(amount)<1:
            await interaction.response.send_message("Min bet set at 1")
        user = self.client.dbHan.getUser(interaction.user.id)
        user=user[0]
        if user[1] < int(amount):
            await interaction.response.send_message("lacking funds")
            return 0
        
        symbols = ["melon","pear","peach","orange","lemon","cherries","grapes","crown"]
        symbolEmoji = {
            "melon":"🍈",
            "pear":"🍐",
            "peach":"🍑",
            "orange":"🍊",
            "lemon":"🍋",
            "cherries":"🍒",
            "grapes":"🍇",
            "crown":"👑"
        }
        amount = int(amount)
        
        self.client.dbHan.increaseCurrency(interaction.user.id,-amount)
        symbol1 = symbols[random.randint(0,7)]
        symbol2 = symbols[random.randint(0,7)]
        symbol3 = symbols[random.randint(0,7)]
        try:
            count = {}
            count[symbol1] = 1
            if symbol2 == symbol1:
                count[symbol1] = 2
            else:
                count[symbol2] = 1
            if symbol3 in count:
                count[symbol3] = count.get(symbol3)+1
            else:
                count[symbol3] = 1
        except Exception as e:
            print("problem in counts")
            print(e)

        try:
            
            if len(count) == 1:
                if 'crown' in count:
                    jackpot = self.client.dbHan.getJackpot()
                    prize = jackpot
                    self.client.dbHan.setJackpot(0)
                else:
                    prize = amount*20
            elif len(count) == 2:
                prize = amount*5
            elif 'crown' in count:
                prize = amount*2
            else:
                prize = 0
                jackpot = self.client.dbHan.getJackpot()
                self.client.dbHan.setJackpot(math.ceil(amount*0.9)+jackpot)
        except  Exception as e:
            print("problem in finding payout")
        try:
            gameEmbed = discord.Embed(title = "slots",description=symbolEmoji[symbol1]+symbolEmoji[symbol2]+symbolEmoji[symbol3])
            if prize == 0:
                gameEmbed.add_field(name="You lost",value=str(amount))
            else:
                gameEmbed.add_field(name="you won",value=str(prize))
            jackpot = self.client.dbHan.getJackpot()
            gameEmbed.add_field(name="current jackpot",value=jackpot)

            await interaction.response.send_message(embed=gameEmbed)
        except Exception as e:
            print("problem in response")
            print(e)
        



        return


        
    
    

    

async def setup(client):
    await client.add_cog(gamblingCog(client))


