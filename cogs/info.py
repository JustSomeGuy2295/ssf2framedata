import json, requests
import os

import discord
from discord import app_commands
from discord.ext import commands


class Info(commands.Cog):
    """Send informational SSF2 links and formatted displays."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='about')
    async def about_command(self, interaction: discord.Interaction):
        """About SSF2 Frame Data"""
        desc = 'A Discord bot based off the Rivals of Aether Acadamy Mentorbot 3.0, modified by justsomeguy__'
        desc += f'```ml\n{len(self.bot.guilds):,} servers / {len(self.bot.users):,} users```'
        embed = discord.Embed(description=desc)
        embed.set_author(
            name='About SSF2 Framedata',
            icon_url=self.bot.user.display_avatar.url)
        embed.add_field(
            name='Developed by blair, adapted by justsomeguy',
            value='https://github.com/blair-c/Mentorbot3.0\nhttps://github.com/JustSomeGuy2295/SSF2-Framedata',
            inline=False)
        embed.add_field(
            name='Data curated by the SSF2 Framedata team',
            value='',
            inline=False)
        embed.add_field(
            name='Profile picture made by Abby (a.k.a. abbeast)',
            value='https://www.instagram.com/daabbeast',
            inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='craft')
    async def crafts_google_sheets(self, interaction: discord.Interaction):
        """Craft's collated framedata sheets"""
        link = 'https://docs.google.com/spreadsheets/d/19OQka-j6OdKqjibINSZUQ5mrtNyDE2xrD4fqmk1orvA/edit?gid=1085478440#gid=1085478440'
        embed = discord.Embed(
            url=link,
            title='Craft\'s Framedata Directory',
            description='Informational data collected and maintained by craftyfurry.')
        embed.set_thumbnail(url='https://i.imgur.com/ScoQwQk.png')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='angles')
    async def di_max_angles(self, interaction: discord.Interaction):
        '''The DI direction which will give you the maximum angle change'''
        embed = discord.Embed(
            description=
            '`337° to 22°  :  Up & Down `\n'
            '` 22° to 23°  :  Down & Down+Away`\n'
            '` 23° to 44°  :  Down+Away`\n'
            '` 45°         :  Down+Away & Up+In`\n'
            '` 46° to 67°  :  Up+In`\n'
            '` 67° to 68°  :  In & Up+In`\n'
            '` 68° to 112° :  In & Away`'
            )
        embed.set_author(name='The best DI for a given knockback angle')
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='formulas')
    async def formulas_kb_hs_hp(self, interaction: discord.Interaction):
        """SSF2 Formulas for knockback, hitstun, etc"""
        link = 'https://rivals.academy/library/glossary/#knockback'
        embed = discord.Embed(description=
            # Knockback
            ('**Knockback** ```ml\n'
             'BKB + (KB_Scaling × Percent_After_Hit × KB_Adj × 0.12)```'
            # Hitstun
            '\n**Hitstun** ```ml\n'
             'Hitstun_Multiplier × ((BKB × (KB_Adj × 2.4 + 1.6)) + '
             '(KB_Scaling × Percent_After_Hit × KB_Adj × 0.312))```'
            # Hitpause
            '\n**Hitpause** ```ml\n'
             'Base_Hitpause + (Hitpause_Scaling × Percent_After_Hit × 0.05) + Extra_Hitpause```'))
        embed.set_author(name='Rivals Formulas')
        await interaction.response.send_message(content=link, embed=embed)
    
    @app_commands.command(name='meteorsmash')
    async def meteor_info(self, interaction: discord.Interaction):
        """Gives info about meteor smashes in SSF2"""
        embed = discord.Embed(description=
            ('**Angles:**\n'
             'Any angle that sends between 250° and 290°.\n'
             'Any move which sends outside this range is considered a spike.\n\n'
             
             'Meteor cancelling can be performed after 9 frames of entering hitstun (not including hitpause, hitlag, etc).'            
            ))
        embed.set_author(name = 'Meteor Smash Info')
        embed.set_image(url='https://i.imgur.com/ljVnFpg.png')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='angleflippers')
    async def angle_flippers(self, interaction: discord.Interaction):
        """List of angle flipper definitions"""
        link = 'https://rivals.academy/library/glossary/#angle-flippers'
        definitions = ('```glsl\n'
            '0 - Sends at the exact knockback angle every time\n'
            '1 - Sends away from the center of the attacker or projectile\n'
            '2 - Sends toward the center of the attacker or projectile\n'
            '3 - Horizontal knockback sends away from the center of the hitbox\n'
            '4 - Horizontal knockback sends toward the center of the hitbox\n'
            '5 - Horizontal knockback is reversed\n'
            '6 - Horizontal knockback sends away from the center of the attacker or projectile\n'
            '7 - Horizontal knockback sends toward the center of the attacker or projectile\n'
            '8 - Sends away from the center of the hitbox\n'
            '9 - Sends toward the center of the hitbox\n'
            '10 - Sends in the direction the attacker is moving```')
        embed = discord.Embed(title='Angle Flipper Definitions', description=definitions)
        await interaction.response.send_message(content=link, embed=embed)
    
    @app_commands.command(name='teching')
    async def teching(self, interaction: discord.Interaction):
        """Teching frame data comparison"""
        link = 'https://rivals.academy/library/glossary/#teching'
        embed = discord.Embed(description=
            # Tech In Place
            ('**Tech In Place** ```ml\n'
            'Intangible | 1-14       \n'
            'Endlag     | 4          \n'
            'FAF        | 19```'
            # Tech Roll
            '\n**Tech Roll** ```ml\n'
            'Intangible | 1-20    \n'
            'Endlag     | 14      \n'
            'FAF        | 35```'
            # Missed (Hitstun)
            '\n**Missed (Hitstun)** ```ml\n'
            'Endlag | 13            \n'
            'FAF    | 14```'
            # Missed (Tumble)
            '\n**Missed (Tumble)** ```ml\n'
            'Endlag | 7             \n'
            'FAF    | 8```'
            # Wall Tech
            '\n**Wall Tech** ```ml\n'
            'Intangible | 1-15    \n'
            'FAF        | 12      \n'
            'Airdodge/Jump Cancellable 4-11```'
            # Ceiling Tech
            '\n**Ceiling Tech** ```ml\n'
            'Intangible | 1-15       \n'
            'FAF        | 12         \n'
            'IASA Cancellable 1-19```'))
        embed.set_author(name='Universal Teching Frame Data')
        embed.set_image(url='https://cdn.discordapp.com/attachments/'
                            '376248878334214145/1160821640221962341/'
                            'roaknockdownframedata.png')
        await interaction.response.send_message(content=link, embed=embed)

    # Misc.
    @app_commands.command(name='troubleshoot')
    async def fps_fix(self, interaction: discord.Interaction):
        """60 fps fix instructions for Nvidia graphics cards"""
        link = 'https://twitter.com/darainbowcuddle/status/1410724611327631364'
        await interaction.response.send_message(link)

    @app_commands.command(name='replays')
    async def how_to_access_your_replays(self, interaction: discord.Interaction):
        """How to access your SSF2 replays"""
        embed = discord.Embed()
        embed.set_author(
            name='How to Access Your Replays', 
            icon_url=self.bot.user.display_avatar.url)
        embed.add_field(
            name='Method 1:',
            value='1. Press `Win + R`\n'
                  '2. Put in the following: ```%LocalAppData%\\RivalsOfAether\\replays```',
            inline=False)
        embed.add_field(
            name='Method 2:',
            value='1. Make sure "Hidden items" are shown in File Explorer\n'
                  '2. Go to: ```C:\\Users\\yourname\\AppData\\Local\\RivalsofAether\\replays```',
            inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
