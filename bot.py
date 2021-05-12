# bot.py
import os
import asyncio
import logging ### imports all required libraries
import discord
from dotenv import load_dotenv ### lets the program access secure file containing user token
from random import randint
from time import time
from math import ceil,floor

logging.basicConfig(level=logging.INFO) ### activates logging 



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

betactive = False

###coinCreate()

msg = ""

seconds = 0

    
    



winconfirmneeded = False
totalpool = 0 # current total betting pool is set to 0
bet = [] # sets all of these to empty lists to avoid errors when using append
options = []
odds = []
currentbetmessage = ""


async def betUpdate(bet,options,seconds,totalpool,odds,currentbetmessage):
    betmessage = str("<a:cowardcoin:813889535699189871> A BET IS NOW ACTIVE! <a:cowardcoin:813889535699189871>\nYou have "+str(seconds)+" seconds to make your bets by typing 'bet coins (option number) (coins)'!\nThe total betting pool is "+str(totalpool)+".\nYour Options Are:\n")
# <a:cowardcoin:813889535699189871> is the ID for an emote - to change the emote, send a message using your emote of choice with a backslash (\) in front of it, and copy the text that is sent instead of the emote
    for x in range(0,len(options)): # for each option in the bet
        try: # runs this code, and if there's an error runs the code under except
            odds[x] = round((bet[x][1])/totalpool,2) # calculates the specific odds for this option in the bet
        except ZeroDivisionError: # if the code divides by zero (when the total pool is empty)
            odds[x] = 0 # sets the odds to 0 
        betmessage += str("Option "+str(x+1)+": "+str(bet[x][0])+" (Odds: "+str(odds[x])+":1)\n") # writes it in the format: "Option 1: 50 coins (Odds: 0.32:1)"
    await currentbetmessage.edit(content=betmessage) # edits the message to the above format


# sorry i cant remember what most of this code does i was running on 2 hours of sleep when i wrote it and i'm running on 1 right now

async def betCreate():
    global totalpool
    global bet
    global options
    global odds
    global currentbetmessage
    global seconds
    global winconfirmneeded
    # gives the program variables from the rest of the program
    
    print("Creating Bet")
    textfile = open("currentbet.txt","r")
    fulllist = eval(textfile.read())
    textfile.close()
    odds = [] # sets the lists to empty lists - clears out old bets if any remain
    bet  = []
    options = fulllist[0] # sets options to a list inside of the text file containing each option for the bet
    print(options) # prints the options to the log
    timeleft = fulllist[1] # sets timeleft to the numbers set for minutes and seconds in the text file
    seconds = (int(timeleft[0])*60)+int(timeleft[1]) # converts minutes and seconds into plain seconds
    totalpool = 0 # sets the total bet pool to 0
    betactive = True # tells the rest of the program a bet is currently active

    betmessage = str("<a:cowardcoin:813889535699189871> A BET IS NOW ACTIVE! <a:cowardcoin:813889535699189871>\nYou have "+str(seconds)+" seconds to make your bets by typing 'bet coins (option number) (coins)'!\nThe total betting pool is:"+str(totalpool)+"\nYour Options Are:\n") # writes out a message
    for x in range(0,len(options)):
        bet.append(list([options[x],0,[]]))
        print(bet)
        print(x)
        odds.append(1)
        betmessage += str("Option "+str(x+1)+": "+str(bet[x][0])+" (Odds: "+str(odds[x])+":1)\n")


    if maintenence:
        channel = client.get_channel(int(ADMINCHANNEL))
    else:
        channel = client.get_channel(int(COINCHANNEL))
    currentbetmessage = await channel.send(betmessage)

    for y in range(seconds):
        await asyncio.sleep(1)
        seconds=seconds-1
        if seconds == 0:
            await currentbetmessage.edit(content="BET OVER")
        else:
            await betUpdate(bet,options,seconds,totalpool,odds,currentbetmessage)
           
    textfile = open("currentbet.txt","w")
    textfile.close()
    betactive = False

    channel = client.get_channel(int(ADMINCHANNEL))
    await channel.send("Who won?")
    winconfirmneeded = True
        
           
        
        
async def coinCreate():
    global coinavailable,coingiven,msg
    print("creating new coin")
    if coinavailable != True:
        coingiven = False
        file = discord.File(r"C:\Users\jemst\Desktop\Discord Bots\WRTVFC\cowardcoin.gif",filename="cowardcoin.gif")
        print("selected gif file")
        if maintenence == False:
            channel = client.get_channel(int(COINCHANNEL))
        else:
            channel = client.get_channel(int(ADMINCHANNEL))
            
        msg = await channel.send("A New Coin is Available!\nType 'get coin' to claim it!",file=file)
        coinavailable=True
        randomtime = time()+randint(0,1800)

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
    global betactive
    global totalpool
    global bet
    global options
    global odds
    global currentbetmessage
    global seconds
    global winconfirmneeded
    
    admin = False
    for roles in message.author.roles: # for each role the author of the message has:
        if roles.id == 726850875913666560 or roles.name == "admins": # if the role has the ID of the admin channel (change this for your server):
            admin = True # sets the variable "admin" for this message specifically to true
            break # ends the for loop - we got what we came for, the user is an admin
        
    
    if message.author == client.user:
        return
### if the author is the bot, cancel everything
    
    if int(message.guild.id) == int(GUILDID): # if the message is in the pre-set server: (all code for messages should be within this if statement)

        if admin:
            print(message.author.name+" (admin) in "+message.channel.name+": "+message.content)
        else:
            print(message.author.name+": "+message.content)  

            
        readmsg = message.content.lower() # sets readmsg to the content of the message, in all lower case

        if admin and readmsg.startswith("cancel bet"):
            textfile = open("currentbet.txt","w")
            textfile.close()
            betactive = False

        if admin and (readmsg.startswith("confirm") or readmsg.startswith("yes")) and confirmationneeded:
            confirmationneeded == False
            await betCreate()
        elif confirmationneeded == True:
            confirmationneeded == False

                
        
        
        if readmsg.startswith("create coin") and admin: # if the user is an admin AND the message starts with "create coin",
            await coinCreate() # runs the subroutine to create a coin. await means it can run asynchronously

            
        if readmsg.startswith("get coin"):
                if coinavailable and coingiven == False:
                    coinscreated = 0
                    coingiven = True
                    textfile = open("coins.txt","r")
                    coins = eval(textfile.read())
                    textfile.close()
                    coinsadd = randint(150,350)
                    try:
                        coins[message.author.id] = coins[message.author.id]+coinsadd
                    except KeyError:
                        coins[message.author.id] = coinsadd
                    
                    textfile = open("coins.txt","w")
                    textfile.write(str(coins))
                    textfile.close()
                    
                    await message.channel.send("<a:cowardcoin:813889535699189871> | "+message.author.mention+" collected "+str(coinsadd)+" CowardCoins!")
                    await message.delete()
                       
                    await msg.delete()
                    coinavailable = False

        
        if readmsg.startswith("coin count"):
            author = message.author.name
            authorid = message.author.id
            textfile = open("coins.txt","r")
            coins = eval(textfile.read())
            textfile.close()
            textfile = open("messagessent.txt","r")
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


        if readmsg.startswith("coin bet create") and admin:
            options = readmsg.split("#")
            print(len(options))
            textfile = open("currentbet.txt","r")
            if textfile.read() == "":
                if len(options) >= 5:
                    del options[0]
                    minutes = options[-2]
                    seconds = options[-1]
                    print(time)
                    del options[-1]
                    del options[-1]
                    textfile = open("currentbet.txt","w")
                    textfile.write("["+str(options)+",["+str(minutes)+","+str(seconds)+"]]")
                    await message.channel.send("options: "+str(options)+"\ntime: "+str(minutes)+" minutes and "+str(seconds)+" seconds\nIs this correct?")
                    confirmationneeded = True
                    

                else:
                    await message.channel.send("Incorrect Format")
                        

                    
                print(message.author.roles)

            else:
                await message.channel.send("A bet is already in progress <:waynerSob:726571399275085895>")
            
            
        if readmsg.startswith("bet coins "):
            if True:
                text = readmsg.split(" ")
                
                try:
                    coinsspent = int(text[-1])
                    optionchosen = int(text[-2])
                    optionchosen = optionchosen-1
                except:
                    await message.channel.send("One of those is formatted incorrectly! They should both be numbers.")
                    return
                
                try:
                    await message.channel.send("betting "+text[-1]+" coins on '"+(str(options[optionchosen]))+"'")
                except IndexError:
                    await message.channel.send("Something went wrong! Is your command structured 'bet coins (option) (coins)?' Or is that a listed option?")
                    return
                textfile = open("coins.txt","r")
                coins = eval(textfile.read())
                textfile.close()
                if coins[message.author.id] >= coinsspent and optionchosen <= len(options):
                    coins[message.author.id] -= coinsspent
                    textfile = open("coins.txt","w")
                    textfile.write(str(coins))
                    textfile.close()
                    totalpool += coinsspent
                    bet[optionchosen][1] += coinsspent
                    if message.author.id in bet[optionchosen][2]:
                        print("already made a bet")
                    else:
                        bet[optionchosen][2].append(message.author.id)
                    print(bet)
                    await betUpdate(bet,options,seconds,totalpool,odds,currentbetmessage)
                    
                    
                else:
                    await message.channel.send("You don't have enough coins!")
                
        
        textfile = open("messagessent.txt","r")
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
            textfile = open("coins.txt","r")
            coins = eval(textfile.read())
            textfile.close()
            try:
                coins[message.author.id] = coins[message.author.id]+coinsadd
            except KeyError:
                coins[message.author.id] = coinsadd
            textfile = open("coins.txt","w")
            textfile.write(str(coins))
            textfile.close()
            await asyncio.sleep(5)
            coindrop = False
            await msg.delete()

        textfile = open("messagessent.txt","w")
        textfile.write(str(messagessent))
        textfile.close()
        currenttime = time()
        if currenttime >= randomtime and coinscreated == 0:
            coinscreated += 1
            await coinCreate()

        if winconfirmneeded:
            if admin:
                try:
                    winner = int(message.content)-1
                except:
                    message.channel.send("error")
                    return
                if maintenence:
                    channel = client.get_channel(813839392342671371)
                else:
                    channel = client.get_channel(813898229368094760)


                winnings = ceil(totalpool/len(bet[winner][2]))
                await channel.send("'"+options[winner]+"' won!")
                await channel.send("Each of the following wins "+str(winnings)+" coins:")

                print(bet)
                print(bet[winner])
                print(bet[winner][0])
                textfile = open("coins.txt","r")
                coins = eval(textfile.read())
                textfile.close()
                for user in bet[winner][2]:
                    print(user)
                    member = await client.fetch_user(user)
                    print(member)
                    await channel.send(member.mention)
                    coins[user] = coins[user]+winnings
                
                
                textfile = open("coins.txt","w")
                textfile.write(str(coins))
                textfile.close()
                
        
            
                



client.run(TOKEN)
