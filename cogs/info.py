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
            '```py\n337° to 22°  :  Up & Down \n 22° to 23°  :  Down & Down+Away\n 23° to 44°  :  Down+Away\n 45°         :  Down+Away & Up+In\n 46° to 67°  :  Up+In\n 67° to 68°  :  In & Up+In\n 68° to 112° :  In & Away```'
            )
        embed.set_author(name='The best DI for a given knockback angle')
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='formulas')
    async def formulas_kb_hs_hp(self, interaction: discord.Interaction):
        """SSF2 Formulas for knockback, hitstun, etc"""
        embed = discord.Embed(description=
            (
            '**NOT CHANGED TO REFLECT SSF2 FRAMEDATA**'
            # Knockback
            '\n**Knockback** ```ml\n'
             'BKB + (KB_Scaling × Percent_After_Hit × KB_Adj × 0.12)```'
            # Hitstun
            '\n**Hitstun** ```ml\n'
             'Hitstun_Multiplier × ((BKB × (KB_Adj × 2.4 + 1.6)) + '
             '(KB_Scaling × Percent_After_Hit × KB_Adj × 0.312))```'
            # Hitpause
            '\n**Hitpause** ```ml\n'
             'Base_Hitpause + (Hitpause_Scaling × Percent_After_Hit × 0.05) + Extra_Hitpause```'))
        embed.set_author(name='SSF2 Formulas')
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name='meteorsmash')
    async def meteor_info(self, interaction: discord.Interaction):
        """Gives info about meteor smashes in SSF2"""
        embed = discord.Embed(description=
            ('**Angles:**\n'
             'Any angle that sends between 250° and 290°.\n'
             'Any move which sends outside this range is considered a spike.\n\n'
             
             'Meteor cancelling is when a double jump or up special is performed while in hitstun from a meteor smash.'
             'Meteor cancelling can be performed after 9 frames of entering hitstun (not including hitpause, hitlag, etc).'
             'Attempting a meteor cancel too early results in a lockout and you cannot attempt to meteor cancel again until you leave hitstun.'            
            ))
        embed.set_author(name = 'Meteor Smash Info')
        embed.set_image(url='https://i.imgur.com/ljVnFpg.png')
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='teching')
    async def teching(self, interaction: discord.Interaction):
        """Information about teching"""
        embed = discord.Embed(description=
            # Tech on surface
            ('**Tech on Surface**\n'
            'There is a 10 frame buffer to allow you to tech. \n'
            'Going out of hitstun resets the buffer window.\n'
            # Tech lockout
            '\n**Tech Lockout**\n'
            'After attempting a tech and failing you are unable to tech for 12 frames\n'
            # Ground Bounce
            '\n**Ground Bounce**\n'
            'When missing the tech on a meteor smash you will bounce on the stage while still being in hitstun. The window to tech the bounce is 1 frame.\n'

            # Wall Tech
            '\n**Wall Tech**'
            '\nWall techs recover instantly, if teching off a wall gravity takes effect immediately.'
            )
        )
        embed.set_author(name='Universal Teching Frame Data')
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name='clanking')
    async def clanking(self, interaction: discord.Interaction):
        """Informatino about clanking"""
        embed = discord.Embed(description=
            ('**Clanking**\n'
             'If two attacks collide and the damage values are within 8% of each other both characters will recoil.\n'
             'If the clank involves a projectile the projectile will simply be cancelled out without causing recoil.\n'
             'Physical air attacks cannot clank with other physical attacks.\n'
             
             '\n**Out-Prioritizing**\n'
             'When the difference in damage is greater than 8% the stronger attack cancels out the weaker attack.\n'
             'Between physical attacks the weaker one will enter recoil, while the stronger attack will continue.\n'
             'Between two projectiles the stronger projectile will cancel out the weaker one and continue as normal.\n'
             'Between a projectile and physical attack a stronger projectile will simply ignore the attack, while a weaker projectile will be cancelled out without causing a clank.'
            )                      
        )
        embed.set_author(name='Universal Clanking Information')
        await interaction.response.send_message(embed=embed)
        
    # Misc.
#    @app_commands.command(name='troubleshoot')
#    async def fps_fix(self, interaction: discord.Interaction):
#        """60 fps fix instructions for Nvidia graphics cards"""
#        link = 'https://twitter.com/darainbowcuddle/status/1410724611327631364'
#        await interaction.response.send_message(link)

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
