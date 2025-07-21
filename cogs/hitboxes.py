import json, requests
from typing import Literal

import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands
from tabulate import tabulate

import sqlite3

class HitboxView(View):
    def __init__(self, embeds, gif_pairs, hits, user: discord.User):
        super().__init__()
        self.embeds = embeds  # list of discord.Embed objects
        self.gif_pairs = gif_pairs  # list of tuples: (fullspeed_url, slowmo_url)
        self.hits = hits
        self.current_hit = 0
        self.user = user

        # GIF Speed Buttons
        self.add_item(GIFSpeedToggle("Full Speed", True, self))
        self.add_item(GIFSpeedToggle("Slow", False, self))
        
        # Hit buttons
        for idx, embed in enumerate(embeds):
            hit_name = hits[idx] if hits[idx] else f"Hit {idx+1}"
            self.add_item(MoveSelect(hit_name, idx, self))

    def get_current_embed(self):
        return self.embeds[self.current_hit]

    def get_current_gif(self, slowmo: bool):
        urls = self.gif_pairs[self.current_hit]
        return urls[1] if slowmo else urls[0]

class GIFSpeedToggle(Button):
    def __init__(self, name: str, is_fullspeed: bool, view: HitboxView):
        self.is_fullspeed = is_fullspeed
        self.custom_view = view
        style = discord.ButtonStyle.blurple
        super().__init__(label=name, style=style)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.custom_view.user:
            await interaction.response.send_message("You're not allowed to use this button.", ephemeral=True)
            return

        idx = self.custom_view.current_hit
        embed = self.custom_view.get_current_embed()
        embed.set_image(url=self.custom_view.get_current_gif(slowmo=not self.is_fullspeed))
        await interaction.response.edit_message(embed=embed, view=self.custom_view)
        
class MoveSelect(Button):
    def __init__(self, name: str, index: int, view: HitboxView):
        self.index = index
        self.custom_view = view
        super().__init__(label=name, style=discord.ButtonStyle.gray)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.custom_view.user:
            await interaction.response.send_message("You're not allowed to use this button.", ephemeral=True)
            return

        self.custom_view.current_hit = self.index
        embed = self.custom_view.get_current_embed()
        # Set default image to full speed
        embed.set_image(url=self.custom_view.get_current_gif(slowmo=False))
        await interaction.response.edit_message(embed=embed, view=self.custom_view)


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
    gif_pairs = []  # (fullspeed_url, slowmo_url)
    hits = []

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
        hit_text = f" ({row[0]})" if row[0] else ""
        embed.set_author(name=f'{char} {move}{hit_text}', icon_url=icon)
        embed.set_footer(text='Up to date as of patch 1.4.0.1')
        embed.set_image(url=row[7])  # Default to fullspeed

        embeds.append(embed)
        gif_pairs.append((row[7], row[15]))  # (fullspeed, slowmo)

    view = HitboxView(embeds, gif_pairs, hits, user)
    return embeds[0], view


    # Creating buttons

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

    # Hits buttons
    for idx, embed in enumerate(embeds):
        hit_name = hits[idx] if hits[idx] else f"Hit {idx+1}"
        self.add_item(MoveSelect(hit_name, idx, self))
        
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

async def setup(bot: commands.Bot):
    await bot.add_cog(Hitboxes(bot))
