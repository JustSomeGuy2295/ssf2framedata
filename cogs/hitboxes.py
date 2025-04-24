import json, requests
from typing import Literal

import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands
from tabulate import tabulate

import sqlite3

class MoveSelect(Button):
    def __init__(self, name: str, embed: discord.Embed, user: discord.User):
        self.embed = embed
        self.user = user
        super().__init__(label=name, style=discord.ButtonStyle.gray)

    async def callback(self, interaction: discord.Interaction):
        if self.user == interaction.user:
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("You're not allowed to use this button.", ephemeral=True)

class GIFSpeed(Button):
    def __init__(self, name: str, embed: discord.Embed, user: discord.User):
        self.embed = embed
        self.user = user
        super().__init__(label=name, style=discord.ButtonStyle.blurple)
        
    async def callback(self, interaction: discord.Interaction):
        if self.user == interaction.user:
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("You're not allowed to use this button.", ephemeral=True)

def ssf2_hitbox(char: str, move: str, user: discord.User):
    '''
    The function used by the character commands to collect the data required
    
    Returns:
        A discord embed
    '''
    con = sqlite3.connect("C:/Users/jesas/Documents/SSF2/ssf2framadata.com/ssf2framedata/data/academy.db")
    cur = con.cursor()

    db_char_id = cur.execute("SELECT id FROM characters WHERE name=?", (char,)).fetchone()[0]
    db_move_id = cur.execute("SELECT id FROM moves WHERE display_name=?", (move,)).fetchone()[0]
    character_data = cur.execute("SELECT color, icon FROM characters WHERE name=?", (char,)).fetchone()
    color = int(character_data[0], 16)
    icon = character_data[1]

    hitboxes = cur.execute("""
        SELECT hit, startup, active, endlag, damage, faf, landing_lag, image, 
               sourspot_damage, sweetspot_damage, tipper_damage, notes,
               intangible, invulnerable, armored, slowmo
        FROM hitboxes 
        WHERE char_id=? AND move_id=?
    """, (db_char_id, db_move_id)).fetchall()

    con.close()

    embeds = []
    hits = []
    view = View()

    # Defining embed info
    for idx, row in enumerate(hitboxes):
        hits.append(row[0])
        
        info = {
            'Startup': row[1], 'Active': row[2], 'Endlag': row[3],
            'Damage': row[4], 'FAF': row[5], 'Landing Lag': row[6],
            'Sourspot Damage': row[8], 'Sweetspot Damage': row[9], 'Tipper Damage': row[10],
            'Intangible': row[12], 'Invulnerable': row[13], 'Armored': row[14],
            'Notes': row[11]
        }

        desc = "\n".join(f"{k}: {v}" for k, v in info.items() if v is not None)
        embed = discord.Embed(description=f'```py\n{desc}```', color=color)
        hit_text = f" ({hits[idx]})" if hits[idx] else ""
        embed.set_author(name=f'{char} {move}{hit_text}', icon_url=icon)
        embed.set_footer(text='Up to date as of patch 1.3.1.2')
        embed.set_image(url=row[7])

        embeds.append(embed)

    # Creating buttons
    '''
    As of now there is no satisfactory way to collect GIFs
    CE hitbox frames are not all centred correctly
    1.3.1.1 training mod doesn't work to the full capacity wanted
    Modding the game myself hasn't worked properly

    # Slowmo button    
    if row[7]:
            fullspeed_embed = embed.copy()
            fullspeed_embed.set_image(url=row[7])
            view.add_item(GIFSpeed("Full Speed", fullspeed_embed, user))
    # Full speed button
    if row[15]:
            slow_embed = embed.copy()
            slow_embed.set_image(url=row[15])
            view.add_item(GIFSpeed("Slow", slow_embed, user))

    '''

    # Hits buttons
    for idx, embed in enumerate(embeds):
        if hits[idx]:
            view.add_item(MoveSelect(f"{hits[idx]}", embed, user))

    return embeds[0], view

class Hitboxes(commands.Cog):
    """Send displays of frame data, character, and hitbox info."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Bandana Dee
    moves = Literal[
        'Jab', 'Dash Attack',
        'Down Tilt', 'Up Tilt', 'Forward Tilt',
        'Neutral Air', 'Down Air', 'Up Air', 'Forward Air', 'Back Air',
        'Down Smash', 'Up Smash', 'Forward Smash', 
        'Up Special', 'Neutral Special',
        'Down Special', 'Side Special',
        'Grab', 'Forward Throw', 'Back Throw', 'Up Throw', 'Down Throw'
    ]

    @app_commands.command(name='bandanadee')
    async def bandanadee(self, interaction: discord.Interaction, attack: moves):
        """Bandana Dee frame data and hitbox info"""
        ssf2_embed, view = ssf2_hitbox('Bandana Dee', attack, interaction.user)
        await interaction.response.send_message(embed=ssf2_embed, view=view)
        
    # Black Mage
    moves = Literal[
        'Jab', 'Dash Attack',
        'Down Tilt', 'Up Tilt', 'Forward Tilt',
        'Neutral Air', 'Down Air', 'Up Air', 'Forward Air', 'Back Air',
        'Down Smash', 'Up Smash', 'Forward Smash', 
        'Up Special', 'Neutral Special',
        'Down Special', 'Side Special',
        'Grab', 'Forward Throw', 'Back Throw', 'Up Throw', 'Down Throw'
    ]

    @app_commands.command(name='blackmage')
    async def blackmage(self, interaction: discord.Interaction, attack: moves):
        """Black Mage frame data and hitbox info"""
        ssf2_embed, view = ssf2_hitbox('Black Mage', attack, interaction.user)
        await interaction.response.send_message(embed=ssf2_embed, view=view)
        
    # Sonic
    moves = Literal[
        'Jab', 'Dash Attack',
        'Down Tilt', 'Up Tilt', 'Forward Tilt',
        'Neutral Air', 'Down Air', 'Up Air', 'Forward Air', 'Back Air',
        'Down Smash', 'Up Smash', 'Forward Smash', 
        'Up Special', 'Neutral Special',
        'Down Special', 'Side Special',
        'Grab', 'Forward Throw', 'Back Throw', 'Up Throw', 'Down Throw'
    ]

    @app_commands.command(name='sonic')
    async def sonic(self, interaction: discord.Interaction, attack: moves):
        """Sonic frame data and hitbox info"""
        ssf2_embed, view = ssf2_hitbox('Sonic', attack, interaction.user)
        await interaction.response.send_message(embed=ssf2_embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Hitboxes(bot))
