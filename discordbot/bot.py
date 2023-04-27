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
        ranked_status_player = watcher.league.by_summoner(my_region, status['id']) #have one more dict in this list
        champid = watcher.champion_mastery.by_summoner(my_region, status['id'])
        latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
        static_champion_list = watcher.data_dragon.champions(latest, False, 'pt_BR')
        champ_key = champid[0]['championId']
        embed = discord.Embed(title=status['name'], type='rich')

        solo_queue = None

        for queue in ranked_status_player:
            if queue['queueType'] == 'RANKED_SOLO_5x5':
                solo_queue = queue
                break
        
        if solo_queue:
            embed.add_field(inline=False, name='Queue Type', value='Solo/Duo')
            embed.add_field(inline=True, name='Wins', value=str(solo_queue['wins']))
            embed.add_field(inline=True, name='Losses', value=str(solo_queue['losses']))
            embed.add_field(inline=True, name='LPs', value=str(solo_queue['leaguePoints']))
            embed.add_field(inline=True, name='Tier', value=str(solo_queue['tier']))
            embed.add_field(inline=True, name='Rank', value=str(solo_queue['rank']))

            wins = int(solo_queue.get('wins'))
            losses = int(solo_queue.get('losses'))
            win_rate = (wins/losses)

            embed.add_field(inline=True, name='Win Rate', value=("%.2f" % win_rate))
            embed.add_field(inline=False, name='', value='')
            champion_name = next((champ['name'] for champ in static_champion_list['data'].values() if champ['key'] == str(champ_key)), None)
            '''
            champ['name'] is getting the value of name in static_champion_list (dictionary).
            So when 'if' starts, the id from static_champion_list stored on champ will pass through an equal test, confirming if champ['key'] is equal to champions key.
            '''
            if champion_name:
                embed.add_field(inline=True, name="Main Champ", value=champion_name)
            mastery_points = champid[0]['championPoints']
            embed.add_field(inline=True, name='Mastery Points', value=(f"{mastery_points:,}".replace(',', '.')))
        elif IndexError:
            embed.add_field(name='No Rank', value=(f"{player} has no flex ranked matches yet, try !lolflex."))
        else:
            embed.add_field(name='No Matches', value=(f"{player} has no matches yet."))
        await ctx.send(embed=embed)

    except ApiError as e:
        await ctx.send(f'Error: {e}')

@bot.command()
async def lolflex(ctx, *, player):
    api_key = league_of_legendsAPI
    watcher = LolWatcher(api_key)
    my_region = 'br1'
    try:

        status = watcher.summoner.by_name(my_region, player)
        ranked_status_player = watcher.league.by_summoner(my_region, status['id'])
        champid = watcher.champion_mastery.by_summoner(my_region, status['id']) #retorna 240(id) -> kled
        latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion'] #get lol's last version about 'n' and about the champions
        static_champion_list = watcher.data_dragon.champions(latest, False, 'pt_BR') #get champions static info
        champ_key = champid[0]['championId']

        embed = discord.Embed(title=status['name'], type='rich')
        
        flex_queue = None  # variável para armazenar a fila solo encontrada, se houver
        
        for queue in ranked_status_player:
            if queue['queueType'] == 'RANKED_FLEX_SR':
                flex_queue = queue
                break 
        
        if flex_queue:
            embed.add_field(inline=False, name="Queue Type", value='Flex')
            embed.add_field(inline=True, name='Wins', value=str(flex_queue['wins']))
            embed.add_field(inline=True, name='Losses ', value=str(flex_queue['losses']))
            embed.add_field(inline=True, name='LPs', value=str(flex_queue['leaguePoints']))
            embed.add_field(inline=True, name='Tier', value=str(flex_queue['tier']))
            embed.add_field(inline=True, name='Rank', value=str(flex_queue['rank']))

            wins = int(flex_queue.get('wins'))
            losses = int(flex_queue.get('losses'))
            win_rate = (wins/losses)

            embed.add_field(inline=True, name='Win Rate', value=("%.2f" % win_rate))
            embed.add_field(inline=False, name='', value='')
            champion_name = next((champ['name'] for champ in static_champion_list['data'].values() if champ['key'] == str(champ_key)), None)
            if champion_name:
                embed.add_field(inline=True, name="Main Champ", value=champion_name)
            mastery_points = champid[0]['championPoints']
            embed.add_field(inline=True, name='Mastery Points', value=(f"{mastery_points:,}".replace(',', '.')))
        elif IndexError:
            embed.add_field(name='No Rank', value=(f"{player} has no flex ranked matches yet, try !lol."))
        else:
            embed.add_field(name='No Matches', value=(f"{player} has no ranked matches yet."))
        await ctx.send(embed=embed)

    except ApiError as e:
        await ctx.send(f'Error: {e}')


bot.run(BOTTOKEN.bottoken)


