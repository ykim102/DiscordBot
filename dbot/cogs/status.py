import discord
from discord.ext import commands

class stat(commands.Cog):

    def __init__(self, client):
        self.client = client

#================================================================================#
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is running normally.')
#================================================================================#

#================================================================================#
    #Check bot latency from the server, taken from API
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Bot latency at {round(self.client.latency * 1000)}ms.')
#================================================================================#

#================================================================================#
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.logout()
#================================================================================#

def setup(client):
    client.add_cog(stat(client))
