import discord
from discord.ext import commands


class PingCog(commands.cog):
    def __init__(self, client):
        self.client = client


@commands.Cog.listener("on_ready")
async def on_ready(self):
    print(f'{self.client.user}, Bot is online!')


@commands.command(name='ping', help='This command returns the latency')
async def ping(self, ctx):
    await ctx.send(f'**Pong!** Latency: {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(PingCog(client))
