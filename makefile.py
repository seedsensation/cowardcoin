print("Do you already know how to make a bot, or already have one? Type 'yes' if you do, otherwise I'll walk you through how to get a bot set up.")
yn = input(">_")
if yn.lower() != "yes":
    print("This file will walk you through, step by step, creating an environment for CowardCoin to run.")
    print("Step 1: Create a Discord Account.")
    print("Once you've completed each step, press enter.")
    input("")
    print("Go to http://discord.com/developers.")
    input("")
    print("Click on the blue 'New Application' button in the top right corner.")
    print("Name the application you create whatever you want.")
    input("")
    print("Click on the 3 lines in the top left corner, then click on Bot.")
    print("Then, click 'Add Bot'.")
    print("Click on 'Copy' under Token in the new bot menu.")
    print("Paste that in here:")
    token = input(">_")
    print("Open the drop down menu again, and select 'OAuth2'.")
    input("")
    print("Scroll down to OAuth2 URL Generator, and tick the 'bot' box.")
    print("Tick whatever permissions you think the bot should need. If you're not sure, just choose administrator.")
    input("")
    print("Copy the link it gives you, and paste it into your address bar. Choose any server you're an admin for to invite that bot to your server.")
    input("")
    print("Go into Discord settings, and under advanced, enable 'Developer Mode'.")
    input("")
    print("Right click on the icon of the server you invited the bot to, and click 'Copy ID'.")
    print("Paste the result here:")
    guildid = input(">_")
    print("Create a channel specifically for testing the bot, in case of issues.")
    input("")
    print("Right click that channel, click 'Copy ID', then paste the result here:")
    adminchannel = input(">_")
    print("Create a channel specifically for the bot to send coins.")
    print("Right click that channel, click 'Copy ID', then paste the result here:")
    coinchannel = input(">_")
    print("You're all set!")
    

token = input("Please enter your Bot Token:\n>_")
guildid = input("Please enter the ID of the server you've invited the bot to:>_")
adminchannel = input("Please enter the ID of the channel you'll use to test the bot:\n>_")
coinchannel = input("Please enter the ID of the channel you'll use to send coins:\n>_")

print("Creating .env ...")
env = open(".env","w")
env.close()

env = open(".env","a")
env.write("# .env\n")
env.write("DISCORD_TOKEN="+str(token)+"\n")
env.write("DISCORD_GUILD_ID="+str(guildid)+"\n")
env.write("ADMIN_CHANNEL="+str(adminchannel)+"\n")
env.write("COIN_CHANNEL="+str(coinchannel)+"\n")
env.close()
