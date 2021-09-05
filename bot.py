# bot.py
import os
import asyncio
import logging ### imports all required libraries
import discord
from dotenv import load_dotenv ### lets the program access secure file containing user token
from random import randint
from time import *
from math import ceil,floor
import datetime
from pathlib import Path

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

msg = ""

coinchance = 0

seconds = 0

def updateCoins(coins):
    textfile = open("files\\coins.txt","w")
    textfile.write(str(coins))
    textfile.close()
    filepath = str("backups\\"+str(datetime.date.today()))
    Path(filepath).mkdir(parents=True,exist_ok=True)
    textfile = open(str(filepath+"\\"+str(datetime.datetime.now().strftime("%H-%M-%S"))+".txt"),"w")
    textfile.write(str(coins))
    textfile.close()


async def coinCreate():
    global coinavailable,coingiven,randomtime,coinscreated,msg,coinchance
    print("creating new coin")
    if coinavailable != True:
        coingiven = False
        coinchance = randint(1,100)
        if coinchance == 1:
            file = discord.File("files\\ultrarare.gif",filename="ultrarare.gif")
        elif coinchance <= 20:
            file = discord.File("files\\gold.gif",filename="gold.gif")
        elif coinchance <= 50:
            file = discord.File("files\\silver.gif",filename="silver.gif")
        else:
            file = discord.File("files\\bronze.gif",filename="bronze.gif")
        print("selected gif file")
        if maintenence == False:
            channel = client.get_channel(int(COINCHANNEL))
        else:
            channel = client.get_channel(int(ADMINCHANNEL))

        if coinchance == 1:
            msg = await channel.send("An Ultra-Rare Red Coin is Available!\nType 'get coin' to claim it!",file=file)
        elif coinchance <= 20:
            msg = await channel.send("A Gold Coin is Available!\nType 'get coin' to claim it!",file=file)
        elif coinchance <= 50:
            msg = await channel.send("A Silver Coin is Available!\nType 'get coin' to claim it!",file=file)
        else:
            msg = await channel.send("A Bronze Coin is Available!\nType 'get coin' to claim it!",file=file)
        
        coinavailable=True
        randomtime = time()+randint(60,3600)

        await asyncio.sleep(30)
        coinavailable=False
        coinscreated = 0
        await msg.delete()
        if coinchance == 1:    # red coin
            emote = "<a:redcoin:844545670709772290>"
        elif coinchance <= 20: # gold coin
            emote = "<a:goldcoin:813889535699189871>"
        elif coinchance <= 50: # silver coin
            emote = "<a:silvercoin:844545665911881788>"
        else:                  # bronze coin
            emote = "<a:bronzecoin:844545666201288755>"
        await channel.send(emote+" | The Coin went unclaimed ...")

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
    global randomtime
    global coindrop
    global msg
    global confirmationneeded
    global coinchance
    
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
            logging.info(message.author.name+" (admin) in "+message.channel.name+" ("+str(round(randomtime-currenttime))+" seconds left)")
            print(message.author.name+" (admin) in "+message.channel.name+": "+message.content+" ("+str(round(randomtime-currenttime))+" seconds left)")
        else:
            logging.info(message.author.name+" in "+message.channel.name+" ("+str(round(randomtime-currenttime))+" seconds left)")  
            print(message.author.name+" in "+message.channel.name+": "+message.content+" ("+str(round(randomtime-currenttime))+" seconds left)")
            

            
        readmsg = message.content.lower() # sets readmsg to the content of the message, in all lower case

        if readmsg.startswith("set coins") and maintenence:
            words = readmsg.split(" ")
            textfile = open("files\\coins.txt","r")
            coins = eval(textfile.read())
            textfile.close()
            coins[message.author.id] = int(words[2])
            await message.channel.send("Given "+str(words[2])+"coins to "+str(message.author.name))
            updateCoins(coins)

        if "give" in readmsg and ("coins" in readmsg or "coin" in readmsg):
            words = readmsg.split(" ")
            textfile = open("files\\coins.txt","r")
            coins = eval(textfile.read())
            textfile.close()

            if message.mentions[0].id not in coins:
                await message.channel.send("<a:goldcoin:813889535699189871> | That person doesn't have any coins yet! Try someone else.")
            elif len(message.mentions) == 1:
                sender = message.author
                receiver = message.mentions[0]
                given = []
                for item in words:
     
                    try:
                        given.append(int(item))
                    except:
                        
                        print("error")

                
                if len(given) != 1:
                    await message.channel.send("<a:goldcoin:813889535699189871> | Make sure there's one number in your message!")
                else:
                    given = given[0]
                    
                    if coins[sender.id] < given:
                        await message.channel.send("<a:goldcoin:813889535699189871> | You don't have enough coins!")
                    else:
                        coins[sender.id] = coins[sender.id]-given
                        coins[receiver.id] = coins[receiver.id]+given
                        updateCoins(coins)
                        await message.channel.send("<a:goldcoin:813889535699189871> | Giving "+str(given)+" coins to "+receiver.mention+" from "+sender.mention+" successfully!")
                    

            
        
        if readmsg.startswith("coin settime") and admin:
            words = readmsg.split(" ")
            try:
                timetoset = int(words[2])
                randomtime = time()+timetoset
                await message.channel.send("<a:goldcoin:813889535699189871> | Time changed to "+str(timetoset)+" seconds from now")
            except:
                await message.channel.send("<a:goldcoin:813889535699189871> | There was an error ...")
        
        if readmsg.startswith("create coin") and admin: # if the user is an admin AND the message starts with "create coin",
            await coinCreate() # runs the subroutine to create a coin. await means it can run asynchronously

            
        if readmsg.startswith("get coin"):
                if coinavailable and coingiven == False:
                    coinscreated = 0
                    coingiven = True
                    textfile = open("files\\coins.txt","r")
                    coins = eval(textfile.read())
                    textfile.close()
                    print(coinchance)
                    if coinchance == 1:    # red coin
                        coinsadd = randint(1500,4000)
                        emote = "<a:redcoin:844545670709772290>"
                    elif coinchance <= 20: # gold coin
                        coinsadd = randint(500,1500)
                        emote = "<a:goldcoin:813889535699189871>"
                    elif coinchance <= 50: # silver coin
                        coinsadd = randint(250,500)
                        emote = "<a:silvercoin:844545665911881788>"
                    else:                  # bronze coin
                        coinsadd = randint(1,150)
                        emote = "<a:bronzecoin:844545666201288755>"
                    
                    try:
                        coins[message.author.id] = coins[message.author.id]+coinsadd
                    except KeyError:
                        coins[message.author.id] = coinsadd
                    
                    updateCoins(coins)
                    
                    await message.channel.send(emote+" | "+message.author.mention+" collected "+str(coinsadd)+" CowardCoins!")
                    await message.delete()
                       
                    await msg.delete()
                    await asyncio.sleep(10)
                    coinavailable = False

        if ("coin" in readmsg and ("for me" in readmsg or "please" in readmsg)):
            chance = randint(1,100)
            print(chance)
            if chance <= 10:
                await message.channel.send("no")
            elif chance == 90:
                await coinCreate()

        
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
                    await message.channel.send("<a:goldcoin:813889535699189871> | "+str(hours)+" hours, "+str(minutes)+" minutes and "+str(seconds)+" seconds left")
                else:
                    await message.channel.send("<a:goldcoin:813889535699189871> | "+str(minutes)+" minutes and "+str(seconds)+" seconds left")
            else:
                await message.channel.send("<a:goldcoin:813889535699189871> | "+str(seconds)+" seconds left")



        
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
            await message.channel.send("<a:goldcoin:813889535699189871> | "+message.author.mention+" has "+str(coins[authorid])+" CowardCoins.\n<a:goldcoin:813889535699189871> | You have "+str(goal-current)+" messages to your next CowardCoin drop!")

        if readmsg.startswith("coin help"):
            await message.channel.send("<a:goldcoin:813889535699189871> | 'get coin' - claims the available coin\n<a:goldcoin:813889535699189871> | 'coin count' - show how many coins you have\n<a:goldcoin:813889535699189871> | 'coin help' - shows this list")


        textfile = open("files\\messagessent.txt","r")
        messagessent = eval(textfile.read())
        textfile.close()
        if message.author.bot == False:
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
                msg = await message.channel.send("<a:goldcoin:813889535699189871> | You got +"+str(coinsadd)+" CowardCoins, "+message.author.mention+"!")
                textfile = open("files\\coins.txt","r")
                coins = eval(textfile.read())
                textfile.close()
                try:
                    coins[message.author.id] = coins[message.author.id]+coinsadd
                except KeyError:
                    coins[message.author.id] = coinsadd
                updateCoins(coins)
                await asyncio.sleep(5)
                coindrop = False

            textfile = open("files\\messagessent.txt","w")
            textfile.write(str(messagessent))
            textfile.close()

        
        
            
                



client.run(TOKEN)
