import discord
import logging
from dotenv import load_dotenv
import os
import asyncio

logging.basicConfig(level=logging.INFO)
load_dotenv()
COINCHANNEL = os.getenv('COIN_CHANNEL')
ADMINCHANNEL = os.getenv('ADMIN_CHANNEL')

client = discord.Client()

async def coinCreate(coinscreated,coingiven,randomtime,msg,coinavailable,maintenence):
    print("creating new coin")
    if coinavailable != True:
        coingiven = False
        file = discord.File(r"C:\Users\jemst\Desktop\COWARDCOIN\WRTVFC\cowardcoin.gif",filename="cowardcoin.gif")
        print("selected gif file")
        print(maintenence)
        if maintenence == True:
            COINCHANNEL = ADMINCHANNEL

        print(COINCHANNEL)
        print(client.get_channel(int(COINCHANNEL)))
        channel = client.get_channel(int(COINCHANNEL))
        print(channel)
        msg = await channel.send("A New Coin is Available!\nType 'get coin' to claim it!",file=file)
        coinavailable=True
        randomtime = time()+randint(0,1800)

        await asyncio.sleep(30)
        await msg.delete()
        await channel.send("<a:cowardcoin:813889535699189871> | The Coin went unclaimed ...")
        coinavailable=False
    else:
        print("coin not available")
