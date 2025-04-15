import json, requests
from typing import Literal

import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands
from tabulate import tabulate

import sqlite3

con = sqlite3.connect('data/academy.db')
cur = con.cursor()

for row in cur.execute("SELECT name FROM characters WHERE id=7"):
    print(row)
    
def ssf2_hitbox():
    print("bambi cum and collapse")


'''
class MoveSelect(Button):
    """"""
    def __init__(self, name: str, embed: discord.Embed, user: discord.User):
        self.embed = embed
        self.user = user
        super().__init__(label=name, style=discord.ButtonStyle.gray)

    async def callback(self, interaction):
        if self.user == interaction.user:
            await interaction.response.edit_message(embed=self.embed)
        else:
            return


def move_display(character: str, move: str, user: discord.User):
    """Return an embed and interactive view for a character's move."""
    char = character.lower().replace(' ', '-')
    resp = requests.get(url=f'https://rivals.academy/library/{char}/data.json')
    data = resp.json()
    info = rivals.characters[character]
    move = move.split(' (')[0].replace('/B', '')

'''