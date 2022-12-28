import discord
import asyncio
import time
import os
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
from random import choice
from asyncio import sleep as s

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
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
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


client = commands.Bot(command_prefix='!p ', intents=intents)

TOKEN = 'MTAyOTQ0NTY5MjIxODk0MTQ2MA.GCA4Xv.rtzvOzBzUtgeekxA8ze2BnBm_g8uxW810E4J5k' 

status = ['Jamming out to music!', 'Scam', 'DDoS', 'KALI', 'Phising', 'Eating!', 'Sleeping!', 'Hacking!', 'Coding!', 'Maintenance!']

@client.event
async def on_ready():
    change_status.start()
    print('Bot is online! as Pepper PEW PEW')

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

@client.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.reply(choice(responses))

@client.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.reply(choice(responses))

@client.command(name='credits', help='This command returns the credits')
async def credits(ctx ,member:discord.Member = None):
    if member == None:
        member = ctx.author
    
    name = member.display_name
    fpf = member.display_avatar

    embed = discord.Embed(title="Pepper Develop by.", description="Mangendre Corp. X NES Extrem", colour=discord.Colour.dark_red())
    embed.set_author(name="Click About Me.", 
                     url="https://mgdrxnes.taplink.ws", 
                     icon_url="https://res.cloudinary.com/dfjwuorv1/image/upload/v1670604234/Logo_Tour_Guide_Ilustrasi_Kuning__3_-removebg-preview_lozkhc.png")
    embed.set_footer(text="Thanks for using Pepper Bot!")

    await ctx.reply(embed=embed)

@client.command(name='creditz', help='This command returns the TRUE credits')
async def creditz(ctx):
    await ctx.send('**No one but me, lozer!**')

@client.command(name='play', help='This command plays music')
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    
    embed = discord.Embed(title="Now Playing :", 
                          description=" {}".format(player.title), colour=discord.Colour.dark_purple())
    embed.set_author(name="Just Enjoy", 
                     icon_url="https://res.cloudinary.com/dfjwuorv1/image/upload/v1670603009/Logo_Tour_Guide_Ilustrasi_Kuning__2_-removebg-preview_brhhv3.png")
    await ctx.send(embed=embed)

@client.command(name='stop', help='This command stops the music and makes the bot leave the voice channel')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='pause', help='This command stops the music and makes the bot leave the voice channel')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.pause()

@client.command(name='resume', help='This command stops the music and makes the bot leave the voice channel')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.resume()

@client.command(name='info', help='This command give the information to member')
async def info(ctx ,member:discord.Member = None):
    if member == None:
        member = ctx.author
    
    name = member.display_name
    fpf = member.display_avatar

    embed = discord.Embed(title="Welcome Our Server", description="Pepper Ready to Seshhhh with Smile :) ", colour=discord.Colour.random())
    embed.set_author(name="Hi! Invite Me by Click.", 
                     url="https://discord.com/api/oauth2/authorize?client_id=1029445692218941460&permissions=0&scope=bot", 
                     icon_url="https://res.cloudinary.com/dfjwuorv1/image/upload/v1670601820/Logo_Tour_Guide_Ilustrasi_Kuning__1_-removebg-preview_nn4fon.png")
    embed.set_thumbnail(url=f"{fpf}")
    embed.add_field(name="Hi! Buddy", value=f"{name}", inline=True)
    embed.add_field(name="Command Help !", value="If u need help just command `?help`", inline=False)
    embed.set_footer(text=f"{name} Thanks a bunch !")

    await ctx.reply(embed=embed)
    
@client.command(name='button', help='masih dikembagin')
async def button(ctx):
    # Create the embed message
    embed = discord.Embed(title='Button', description='Click the button to send a message')

    # Add the button
    embed.add_field(name='Button', value='[Click here](https://google.com)', inline=False)

    # Send the message
    await ctx.send(embed=embed)

@client.command(name='remind', help='This command give the remind for information')
async def remind(ctx, time, task):
    def convert(time):
        pos = ['s', 'm', 'h', 'd']
        
        time_dict = {"s":1, "m":60, "h":3600, "d":3600*24}
        
        unit = time[-1]
        
        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2
        return val * time_dict[unit]
    
    converted_time = convert(time)
    
    if converted_time == -1:
        await ctx.send("You didn't answer the time correctly.")
        return
    
    if converted_time == -2:
        await ctx.send("The Time mush be an integer")
        return
    
    await ctx.send(f"Started reminder for **{task}** and will last **{time}**.")
    
    
    await s(converted_time)
    await ctx.reply(f"{ctx.author.mention} your reminder for **{task}** has finished")
    
    
    
@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run(TOKEN)