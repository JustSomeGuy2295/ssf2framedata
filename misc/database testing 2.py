# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 22:36:41 2025

@author: jesas
"""

import json, requests
from typing import Literal

import sqlite3

con = sqlite3.connect('C:/Users/jesas/Documents/SSF2/ssf2framadata.com/ssf2framedata-master/data/academy.db')
cur = con.cursor()

for row in cur.execute("SELECT name FROM characters WHERE id=7"):
    print(row)
    
def ssf2_hitbox(char: str, move: str):
    for row in cur.execute(f"SELECT id FROM characters WHERE name='{char}'"):
        db_char_id = row[0]
        #print(db_char_id)
    for row in cur.execute(f"SELECT id FROM moves WHERE display_name='{move}'"):
        db_move_id = row[0]
        #print(db_move_id)
        
    for row in cur.execute(f"SELECT startup, active, endlag, faf, landing_lag, image FROM hitboxes WHERE char_id={db_char_id} AND move_id={db_move_id}"):
        #print(row)
        move_startup = row[0]
        move_active = row[1]
        move_endlag = row[2]
        move_faf = row[3]
        move_landing_lag = row[4]
        image = row[5]
        
        print(f'Startup       : {move_startup}')
        print(f'Active Frames : {move_active}')
        print(f'Endlag        : {move_endlag}')
        print(f'FAF           : {move_faf}')
        print(f'Landing Lag   : {move_landing_lag}')


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