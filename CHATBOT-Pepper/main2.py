import discord
import os
import asyncio
from discord.ext import commands


os.chdir('D:\Kampus\Semester 5\PROJECT II\APP\Pepper Bot\discord-pepperbot')

client = commands.Bot(command_prefix="!", intents=discord.Intents().all())
@client.event
async def on_ready():
    print("PUYSING")
# for folder in os.listdir("cogs"):
#     if os.path.exists(os.path.join("cogs", folder, "discroot.py")):
#         client.load_extension("cogs.{folder}.discroot"

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"Cogs.{filename[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start("MTAyOTQ0NTY5MjIxODk0MTQ2MA.GCA4Xv.rtzvOzBzUtgeekxA8ze2BnBm_g8uxW810E4J5k")
asyncio.run(main())


# @client.command()
# async def load(extension):
#     await client.load_extension(f'cogs.{extension}')
    
# @client.command()
# async def unload(extension):
#     await client.unload_extension(f'cogs.{extension}')
    