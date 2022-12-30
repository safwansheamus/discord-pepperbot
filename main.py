import discord
import asyncio
import time
import os
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
from random import choice
from asyncio import sleep as s
from dotenv import load_dotenv


# ENV
load_dotenv()

token = os.environ['TOKEN']
# token2 = os.environ['TOKEN2']

#
intents = discord.Intents.all()
intents.presences = True

intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix='', intents=intents)

status = ['Dahar', 'Modol', 'Tunduh', 'Ulin', 'Manre',
          'Matinro', 'Masessa', 'Malippuno', 'Mabobol', 'Mannasu']


@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


@client.event
async def on_ready():
    change_status.start()
    print(f'Bot is online! as {client.user},Pepper PEW PEW')


@client.command()
async def teung(ctx, arg):
    await ctx.send(arg)

# task
# memasukkan fungsi chat gpt ke sini

client.run(token)
