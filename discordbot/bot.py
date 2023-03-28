import discord
from discord.ext import commands

from apikey import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix = '!', intents=intents)

client.run(BOTTOKEN.bottoken)

