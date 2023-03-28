import discord
from discord.ext import commands

from apikeys import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix = '!', intents=intents)

client.run(BOTTOKEN.bottoken)

@client.event
async def on_ready():
    await print(f'We have loged on as {client.user}')

