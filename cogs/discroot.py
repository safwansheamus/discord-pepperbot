import discord
from discord.ext import commands



class Discroot(commands.Cog):
    def __init__(self, client):
        self.client = client


@commands.Cog.listener()
async def on_ready(self):
    print("Bot is online.")


async def setup(client):
    await client.add_cog(Discroot(client))