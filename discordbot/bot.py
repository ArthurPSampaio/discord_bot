import discord
from discord.ext import commands

from apikeys import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged on as {client.user}')

@client.event
async def on_member_join(member):
    channel = client.get_channel(725848521449930816)
    await channel.send(f'Guten morgen {member.mention}.')

client.run(BOTTOKEN.bottoken)