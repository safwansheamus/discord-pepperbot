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

#
intents = discord.Intents.all()
intents.presences = True

intents.message_content = True
intents.voice_states = True

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable="C:\\ffmpeg\\bin\\ffmpeg.exe"), data=data)


client = commands.Bot(command_prefix='', intents=intents)

TOKEN = 'MTAyOTQ0NTY5MjIxODk0MTQ2MA.GCA4Xv.rtzvOzBzUtgeekxA8ze2BnBm_g8uxW810E4J5k'

status = ['Jamming out to music!', 'Scam', 'DDoS', 'KALI', 'Phising',
          'Eating!', 'Sleeping!', 'Hacking!', 'Coding!', 'Maintenance!']


@client.event
async def on_ready():
    change_status.start()
    print(f'Bot is online! as {client.user},Pepper PEW PEW')


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='welcome-channel')
    await channel.reply(f'Welcome {member.mention}!  Ready to jam out? See `!p help` command for details!')


@client.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    await channel.reply(f"Goodbye {member.mention}, thanks for join this server")


@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')


@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run(token)
