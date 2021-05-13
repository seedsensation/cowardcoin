# bot.py
import os
import asyncio
import logging ### imports all required libraries
import discord
from dotenv import load_dotenv ### lets the program access secure file containing user token
from random import randint
from time import *
from math import ceil,floor

if not os.path.exists(strftime("logs\\%Y.%m.%d\\")):
    os.makedirs(strftime("logs\\%Y.%m.%d\\"))
logtime = strftime("%Y.%m.%d\\%H.%M.%S")
file = open("logs\\%s.txt"% logtime,"w")
file.close()
logging.basicConfig(filename="logs\\%s.txt" % logtime,
                level=logging.INFO,
                format='%(levelname)s: %(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S') ### activates logging



maintenence = False ### if maintenence is set to True, it changes how things work slightly and what channels each message are sent in

if maintenence: # if maintenence mode is active:
    randomtime = (time()+99999999999999999) # stops coins from being created instantly when in maintenance mode
else:
    randomtime = time() # makes the first coin appear instantly



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # accesses the discord token
GUILD = os.getenv('DISCORD_GUILD') # accesses the name of the server
COINCHANNEL = os.getenv('COIN_CHANNEL') # accesses the channel id of the channel coins are shown in
ADMINCHANNEL = os.getenv('ADMIN_CHANNEL') # accesses the channel id of the channel used for maintenence
GUILDID = os.getenv('DISCORD_GUILD_ID') # accesses the server id of the server this version of the bot is active in

# env files are used so that the code can be transferred around with no changes needed for each instance,
# and the bot token isn't needed when distributing the code.

client = discord.Client() # sets 'client' to discord

@client.event # on event in discord
async def on_ready(): # when the bot connects
    await client.change_presence(activity=discord.Game(name="the economy 😎")) # sets the bot's status (pic attached - sc1.png)
    
coinavailable = False # resets coin availability

coinscreated = 0 # sets the count of coins created to 0

# this is just a series of simple checks run to make sure each coin is only sent out once, and only received once

coindrop = False

coingiven = False

confirmationneeded = False

firstrun = True

msg = ""

seconds = 0

async def coinCreate():
    global coinavailable,coingiven,msg,randomtime
    print("creating new coin")
    if coinavailable != True:
        coingiven = False
        file = discord.File("files\\cowardcoin.gif",filename="cowardcoin.gif")
        print("selected gif file")
        if maintenence == False:
            channel = client.get_channel(int(COINCHANNEL))
        else:
            channel = client.get_channel(int(ADMINCHANNEL))
            
        msg = await channel.send("A New Coin is Available!\nType 'get coin' to claim it!",file=file)
        coinavailable=True
        randomtime = time()+randint(60,3600)

        await asyncio.sleep(30)
        await msg.delete()
        await channel.send("<a:cowardcoin:813889535699189871> | The Coin went unclaimed ...")
        coinavailable=False
    else:
        print("coin not available")


    






@client.event
async def on_message(message):
    '''
Most of the program is located in this subroutine.
All of this code runs every time a message is sent in any server the bot is in,
and different code is run based on what each message contains.'''
    global coinscreated
    global coingiven
    global coinavailable
    global msg
    global randomtime
    global coindrop
    global confirmationneeded
    global firstrun

    if firstrun:
        firstrun = False
        asyncio.create_task(checkforcoin())
    
    admin = False
    for roles in message.author.roles: # for each role the author of the message has:
        if roles.id == 726850875913666560 or roles.name == "admins": # if the role has the ID of the admin channel (change this for your server):
            admin = True # sets the variable "admin" for this message specifically to true
            break # ends the for loop - we got what we came for, the user is an admin
        
    
    if message.author == client.user:
        return
### if the author is the bot, cancel everything

    currenttime = time()
    if (currenttime >= randomtime or randomtime-currenttime <= 0) and coinscreated == 0:
            coinscreated += 1
            await coinCreate()
    
    if int(message.guild.id) == int(GUILDID): # if the message is in the pre-set server: (all code for messages should be within this if statement)

        if admin:
            print(message.author.name+" (admin) in "+message.channel.name+": "+message.content+" ("+str(round(randomtime-currenttime))+" seconds left)")
        else:
            print(message.author.name+": "+message.content+" ("+str(round(randomtime-currenttime))+" seconds left)")  

            
        readmsg = message.content.lower() # sets readmsg to the content of the message, in all lower case
                
        if readmsg.startswith("coin settime") and admin:
            words = readmsg.split(" ")
            try:
                timetoset = int(words[2])
                randomtime = time()+timetoset
                await message.channel.send("<a:cowardcoin:813889535699189871> | Time changed to "+str(timetoset)+" seconds from now")
            except:
                await message.channel.send("<a:cowardcoin:813889535699189871> | There was an error ...")
        
        if readmsg.startswith("create coin") and admin: # if the user is an admin AND the message starts with "create coin",
            await coinCreate() # runs the subroutine to create a coin. await means it can run asynchronously

            
        if readmsg.startswith("get coin"):
                if coinavailable and coingiven == False:
                    coinscreated = 0
                    coingiven = True
                    textfile = open("files\\coins.txt","r")
                    coins = eval(textfile.read())
                    textfile.close()
                    coinsadd = randint(150,350)
                    try:
                        coins[message.author.id] = coins[message.author.id]+coinsadd
                    except KeyError:
                        coins[message.author.id] = coinsadd
                    
                    textfile = open("files\\coins.txt","w")
                    textfile.write(str(coins))
                    textfile.close()
                    
                    await message.channel.send("<a:cowardcoin:813889535699189871> | "+message.author.mention+" collected "+str(coinsadd)+" CowardCoins!")
                    await message.delete()
                       
                    await msg.delete()
                    await asyncio.sleep(10)
                    coinavailable = False

        if readmsg.startswith("coin timeleft") and admin:
            seconds = round(randomtime-time())
            minutes = seconds/60
            hours = minutes/60
            hours = floor(hours)
            minutes = minutes-(hours*60)
            minutes = floor(minutes)
            seconds=seconds-(minutes*60)
            seconds = floor(seconds)
            
            if floor(minutes) > 0:
                if floor(hours) > 0:
                    await message.channel.send("<a:cowardcoin:813889535699189871> | "+str(hours)+" hours, "+str(minutes)+" minutes and "+str(seconds)+" seconds left")
                else:
                    await message.channel.send("<a:cowardcoin:813889535699189871> | "+str(minutes)+" minutes and "+str(seconds)+" seconds left")
            else:
                await message.channel.send("<a:cowardcoin:813889535699189871> | "+str(seconds)+" seconds left")



        
        if readmsg.startswith("coin count"):
            author = message.author.name
            authorid = message.author.id
            textfile = open("files\\coins.txt","r")
            coins = eval(textfile.read())
            textfile.close()
            textfile = open("files\\messagessent.txt","r")
            messagessent = eval(textfile.read())
            textfile.close()
            author = message.author.name
            authorid = message.author.id
            current = messagessent[authorid][0]
            goal = messagessent[authorid][1]
            if authorid not in coins:
                coins[authorid] = 0
            await message.channel.send("<a:cowardcoin:813889535699189871> | "+message.author.mention+" has "+str(coins[authorid])+" CowardCoins.\n<a:cowardcoin:813889535699189871> | You have "+str(goal-current)+" messages to your next CowardCoin drop!")

        if readmsg.startswith("coin help"):
            await message.channel.send("<a:cowardcoin:813889535699189871> | 'get coin' - claims the available coin\n<a:cowardcoin:813889535699189871> | 'coin count' - show how many coins you have\n<a:cowardcoin:813889535699189871> | 'coin help' - shows this list")


        textfile = open("files\\messagessent.txt","r")
        messagessent = eval(textfile.read())
        textfile.close()
        
        author = message.author.id
        if author not in messagessent:
            messagessent[author] = [0,10]
        if coindrop == False:
            messagessent[author][0] = messagessent[author][0]+1
        if messagessent[author][0] >= messagessent[author][1]:
            coindrop = True
            messagessent[author][0] = 0
            messagessent[author][1] = ceil(messagessent[author][1]*1.25)
            coinsadd = randint(20,50)
            msg = await message.channel.send("<a:cowardcoin:813889535699189871> | You got +"+str(coinsadd)+" CowardCoins, "+message.author.mention+"!")
            textfile = open("files\\coins.txt","r")
            coins = eval(textfile.read())
            textfile.close()
            try:
                coins[message.author.id] = coins[message.author.id]+coinsadd
            except KeyError:
                coins[message.author.id] = coinsadd
            textfile = open("files\\coins.txt","w")
            textfile.write(str(coins))
            textfile.close()
            await asyncio.sleep(5)
            coindrop = False
            await msg.delete()

        textfile = open("files\\messagessent.txt","w")
        textfile.write(str(messagessent))
        textfile.close()

        
async def checkforcoin():
    global randomtime,coinscreated
    print("checking for coin")
    while True:
        print("a")
        currenttime=time()
        print("current time")
        print(currenttime)
        print(randomtime)
        if (currenttime >= randomtime or randomtime-currenttime <= 0) and coinscreated == 0:
            print("the")
            coinscreated += 1
            asyncio.create_task(coinCreate())
            print("theres a coin!")
        
        print("no coin")
        sleep(10)




client.run(TOKEN)

