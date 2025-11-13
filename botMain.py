
import discord
import os
import sys

class botMainClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
    async def on_message(self,message):
        print(message.author)
        if message.author == self:
            pass
        if message.author.id == 690669470171136020:
            await message.add_reaction("🫄")

        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = botMainClient(intents=intents)

client.run()

