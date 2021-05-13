from pathlib import Path
import discord
from discord.ext import commands
import random
import os

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '!', intents = intents)

#================================================================================#
class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Setup complete.")

    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

#================================================================================#
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
#================================================================================#

#================================================================================#
@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not recgonized.')
#================================================================================#

#================================================================================#
#Simple check for bot status on startup
@client.event
async def on_ready():
    print('Bot is ready!')
#================================================================================#

#================================================================================#
#Bot alerts for member join and removals
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
#================================================================================#

#================================================================================#B
@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')
#================================================================================#

#================================================================================#
#Bot plays marco polo with the player, but not really
@client.command()
async def marco(ctx):
    await ctx.send('Polo!')
#================================================================================#


#================================================================================#
#Magic 8-ball function, standard response list taken from Wikipedia
@client.command(aliases = ['8ball'])
async def eightBall (ctx, *, question):
    responses = [   "It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful." ]

    await ctx.send(f'Question: {question}\nMy answer: {random.choice(responses)}')
#================================================================================#



#================================================================================#
#Delete message function (Note:Found some more info on this from https://stackoverflow.com/questions/49159850/deleting-a-bots-message-in-discord-py) - Ryan
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 1):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit = amount + 1)
        await ctx.send("Messages have been removed!", delete_after = 5)
#================================================================================#



#================================================================================#
#Kick and Ban functions, permissions should work OK
@client.command()
async def kick(ctx, member : discord.Member, *, reason = 'No reason provided'):
    if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):
        await member.kick(reason = reason)
        await ctx.send(f'Kicked {member.mention}')
    else:
        await ctx.send("You do not have permissions to do this command")

@client.command()
async def ban(ctx, member : discord.Member, *, reason = 'No reason provided'):
    if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):
        await member.ban(reason = reason)
        await ctx.send(f'Banned {member.mention}')
    else:
        await ctx.send("You do not have permissions to do this command")
#================================================================================#


#================================================================================#
#Unban function
@client.command()
async def unban(ctx, *, member: discord.Member):
    await ctx.guild.unban(member)
    await ctx.send(f'Unbanned {user.mention}')
    return
#================================================================================#


client.run('ODQxNzQ3NDYzOTE5NTAxMzMy.YJrQag.5EP_ccShun8Fab7km47eHhl8c88')
