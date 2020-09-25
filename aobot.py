import discord
from discord.ext import commands
from discord.utils import get
from datetime import date
import asyncio
import random
import os

bot = commands.Bot(command_prefix='.')

############################################################


## Events ##
@bot.event
async def on_ready():
    '''On startup, the bot gives a confirmation message'''
    print('Booting up...\n.\n..\n...\nThe Alpha Omega bot is online.')


## Commands ##
@bot.command()
async def ping(ctx):
    '''Pings the bot and reponds with latency in ms'''
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')





##### Run Bot ######
bot.run(os.environ['token'])