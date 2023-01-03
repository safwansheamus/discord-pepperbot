import discord
import os
from discord.ext import commands, tasks
from random import choice
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.environ['TOKEN2']
TokenDiscord = os.environ['TOKEN']

# Keperluan Memanggil Perintah
intents = discord.Intents.all()
intents.presences = True
intents.message_content = True

# Memanggil Prefix Kalo Menggunakan Prefix dan mengaktifkan
client = commands.Bot(command_prefix='', intents=intents)

# Data dalam fungsi tasks yang akan di looping
status = ['Dahar', 'Modol', 'Tunduh', 'Mannasu', 'Manre',
          'Kobe Oser', 'Ayaine Mambri', 'Nawamar', 'Bolehh']


@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


@client.event
async def on_ready():
    change_status.start()
    print(f'Bot is online! as Pepper PEW PEW')
    


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!openai"):
        inputan = message.content.split()
            
    inputan.pop(0)
    
    hasil = " ".join(inputan)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=hasil,
        temperature=0.9,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    await message.channel.send(response.choices[0].text)

client.run(TokenDiscord)
