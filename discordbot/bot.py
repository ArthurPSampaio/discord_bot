import discord
import openai
import asyncio
from discord.ext import commands
import requests
import json

from apikeys import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# bot = commands.Bot(command_prefix = '!', intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged on as {bot.user}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(725848521449930816)
    await channel.send(f'Guten morgen {member.mention}.')

@bot.command()
async def gpt(ctx: commands.Context, *, prompt: str):
    # verificar se o autor da mensagem é o bot
    if ctx.author.bot:
        return
    openai.api_key = openai_API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=200,
        n=1,
        stop=None,
        timeout=15,
    )
    # enviar resposta do ChatGPT em uma embed
    embed = discord.Embed(title="Resposta:", description=response.choices[0].text, color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else :
        await ctx.send("You must be in a channel to run this command")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        channel = ctx.guild.voice_client
        await channel.disconnect()

@bot.command()
async def img(ctx, *, description):
    # Parâmetros da solicitação HTTP
    data = {
        "model": "image-alpha-001",
        "prompt": description,
        "num_images": 1,
        "size": "1024x1024"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_API}"
    }

    # Enviar a solicitação HTTP
    response = requests.post("https://api.openai.com/v1/images/generations", data=json.dumps(data), headers=headers)

    # Obter a URL da imagem gerada
    image_url = response.json()["data"][0]["url"]

    # Enviar a imagem para o canal do Discord
    embed = discord.Embed(title="Imagem gerada com base na descrição de texto:", description=description)
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

bot.run(BOTTOKEN.bottoken)
