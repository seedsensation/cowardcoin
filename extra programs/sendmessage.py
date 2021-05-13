import os
import asyncio
import logging ### imports all required libraries
import discord
from dotenv import load_dotenv ### lets the program access secure file containing user token
from random import randint
from time import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # accesses the discord token
COINCHANNEL = os.getenv('COIN_CHANNEL')
message = os.getenv('MESSAGE2SEND')

client = discord.Client()

@client.event
async def on_ready():
    while True:
        message = input("")
        channel = client.get_channel(int(COINCHANNEL)) # gets the testing channel
        await channel.send(message)
client.run(TOKEN)
