import discord
import openai
from discord.ext import commands
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



from apikeys import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# client = commands.Bot(command_prefix = '!', intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged on as {bot.user}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(725848521449930816)
    await channel.send(f'Guten morgen {member.mention}.')

@bot.command()
async def gpt(ctx: commands.context, *, prompt: str):
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
async def playfy(ctx, msc, author):
    if ctx.author.bot:
        return
    url = "https://spotify117.p.rapidapi.com/search/"

    querystring = {"keyword":"<REQUIRED>","type":"<REQUIRED>"}

    headers = {
        "X-RapidAPI-Key": spotifyAPI,
        "X-RapidAPI-Host": spotifyHost
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    

bot.run(BOTTOKEN.bottoken)