import discord
import openai
from discord.ext import commands
import requests

from apikeys import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix = '!', intents=intents)
# bot = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged on as {client.user}')

@client.event
async def on_member_join(member):
    channel = client.get_channel(725848521449930816)
    await channel.send(f'Guten morgen {member.mention}.')


@client.command(name='chat')
async def chat_command(ctx, *, message):
    # verificar se o autor da mensagem é o bot
    if ctx.author.bot:
        return

    # enviar mensagem de saudação
    # await ctx.send(f'Olá, eu sou um bot de chat! Você disse: {message}')

    # chamar a API do ChatGPT
    openai.api_key = openai_API
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Conversa: {message}\nBot:",
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
        timeout=15,
    )

    # enviar resposta do ChatGPT
    await ctx.send(response.choices[0].text)


client.run(BOTTOKEN.bottoken)