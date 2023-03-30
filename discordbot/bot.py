# imports
import discord
import openai
import asyncio
import requests
from craiyon import Craiyon, craiyon_utils
from io import BytesIO
import base64
import pandas as pd
import json
# from --- import ---
from discord.ext import commands
from riotwatcher import LolWatcher, ApiError

from apikeys import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

generator = Craiyon()

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
async def img(ctx, *, prompt: str):
    await ctx.send(f"Generating prompt \"{prompt}\"...")
    generated_images = await generator.async_generate(prompt)
    b64_list = await craiyon_utils.async_encode_base64(
        generated_images.images)
    images1 = []
    for index, image in enumerate(b64_list):
        img_bytes = BytesIO(base64.b64decode(image))
        image = discord.File(img_bytes)
        image.filename = f"result{index}.webp"
        images1.append(image)
    await ctx.reply(files=images1)  # dá reply na mensagem do usuário com as 9 imagens geradas

@bot.command()
async def lol(ctx, * ,champion):
    # global variables
    api_key = league_of_legendsAPI
    watcher = LolWatcher(api_key)
    my_region = 'br1'
    champions_url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/data/pt_BR/champion/{champion}.json"
    print(champions_url)
    

bot.run(BOTTOKEN.bottoken)


