from os import getenv
from sys import version
from typing import Literal

import discord
from discord.ext import commands
import redis
import requests
import tabulate

print(f'Python {version}\n'
      f'discord.py {discord.__version__} | '
      f'hiredis-py {redis.__version__} | '
      f'requests {requests.__version__} | '
      f'tabulate {tabulate.__version__}')


class MyBot(commands.Bot):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(
            activity=discord.CustomActivity(name='Beta 1.3.1.2'),
            command_prefix=commands.when_mentioned,
            intents=intents
        )
    
    async def setup_hook(self):
        cogs = [
            'hitboxes',  # Frame data and hitbox commands
            'info',      # Links and info commands
        ]
        for cog in cogs:
            await self.load_extension(f'cogs.{cog}')
            print(f'Loaded {cog} cog...')
        print(f'Logged in as {bot.user}\nUser ID: {bot.user.id}')


intents = discord.Intents.default()
intents.members = True
bot = MyBot(intents=intents)
bot.remove_command('help')

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, scope: Literal['global', 'guild']):
    """Sync global or guild commands"""
    async with ctx.channel.typing():
        if scope == 'global':
            synced = await ctx.bot.tree.sync()
            txt = 'globally'
        elif scope == 'guild':
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            txt = 'to the current guild'
    await ctx.send(f'Synced {len(synced)} commands {txt}')
    
@bot.command()
async def jmac(ctx):
    await ctx.send('Hey guys it\'s me jmac and I really like chairs. You can sit on them, like what the heck! What would we even do without chairs? #chairs\n\n'
                    'Hey guys it\'s me, Jmac again. Tillur said he doesn\'t like chairs! Can you believe it? He must\'ve had a bad time with chairs. Bean bags are cool too. #equality\n\n'
                    'Hey everyone, Jmac here. Paradox just said that tables and the floor are better. I disagree! The chairs are essential for the table. Maybe the floor is also good since it supports the chair! Paradox is on to something. #science\n\n'
                    'Hello guys, it\'s me jmac! captain falco says that stairs are better than chairs. While it does rhyme (which is very cool) I think chairs are better. #chai rs\n\n'
                    'Hi guys! I am jmac. Hida says that when you\'re gaming you sit on chairs. I completely agree. Who stands while gaming? Someone who doesn\'t know the true value of chairs. #purpose\n\n')

@bot.command()
async def doabarrelroll(ctx):
    await ctx.send('https://tenor.com/view/star-fox-star-fox-64-starfox-do-a-barrel-roll-rick-may-gif-3633857843406436610')

if __name__ == '__main__':
    bot.run(getenv('TOKEN'))  # API Key from environment
