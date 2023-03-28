import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix = '!', intents=intents)

client.run('bot token')
print('teste123123123123')
print('teste123123123123')