# imports
import discord
import openai
import base64
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
from craiyon import Craiyon, craiyon_utils
from io import BytesIO

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
async def lol(ctx, *, player):
    api_key = league_of_legendsAPI
    watcher = LolWatcher(api_key)
    my_region = 'br1'
    try:

        status = watcher.summoner.by_name(my_region, player)
        ranked_status_player = watcher.league.by_summoner(my_region, status['id'])
        champion_mastery = watcher.champion_mastery.by_summoner(my_region, status['id'])
        solo_duo = 'RANKED_SOLO_5x5'
        solo_duo_status = watcher.league.entries(my_region, solo_duo, 'GOLD', 'I', 1) + api_search
        print(status)
        print('-------')
        print(ranked_status_player[0]) # [0] get into to the dic and show player's info
        # the error was: it was necessary to access the list first, then manipulate the dict
        embed = discord.Embed(title=status['name'])

        queueType = ranked_status_player[0].get('queueType')
        # ! needs study the api's riot to know how to get RANKED_FLEX_SR at a player who have RANKED_SOLO_5X5 status
        def players_info():
            embed.add_field(inline=True, name='Wins ', value=str(ranked_status_player[0]['wins']))
            embed.add_field(inline=True, name='Losses ', value=str(ranked_status_player[0]['losses']))
            embed.add_field(inline=True, name='Pdls ', value=str(ranked_status_player[0]['leaguePoints']))
            embed.add_field(inline=True, name='Tier ', value=str(ranked_status_player[0]['tier']))
            embed.add_field(inline=True, name='Rank ', value=str(ranked_status_player[0]['rank']))
        
        if queueType == 'RANKED_FLEX_SR':
            embed.add_field(name='No Matches', value=("This player doesn't have solo/duo matches already"))
        elif queueType == 'RANKED_SOLO_5x5':
            players_info()
            
        else:
            await ctx.send('Player not found')
        await ctx.send(embed=embed)
    except ApiError as e:
        await ctx.send(f'Error: {e}')





bot.run(BOTTOKEN.bottoken)


