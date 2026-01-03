import discord
from discord.ext import commands
import random
import re


import sqlite3


TOKEN = input('enter token')

#-------------------------------------------------------------------------------------------------




intents = discord.Intents().all()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
#this may be redundant, but is included just in case further bot. commands are accidentally used in future.
#this should be depreciated to "client."


#bot pre-initialization

client = commands.Bot(command_prefix='$',intents=intents)
#defines prefix and bot intent


#initalizes database
con = sqlite3.connect("charMovement.db")
cur = con.cursor()
#-------------------------------------------------------------------------------------------------
cur.execute("CREATE TABLE IF NOT EXISTS characterLoc(character, movement)")
con.commit()
#-------------------------------------------------------------------------------------------------

# below defines all dictionaries used for the cardGen function
dictSuit = {
    "1": "Orcx",
    "2": "Guns",
    "3": "Suns",
    "4": "Klorxx"
}

dictCards = {
    "1": "Aces (low) of ",
    "2": "1 of ",
    "3": "2 of ",
    "4": "3 of ",
    "5": "4 of ",
    "6": "5 of ",
    "7": "6 of ",
    "8": "7 of ",
    "9": "8 of ",
    "10": "9 of ",
    "11": "10 of ",
    "12": "Snakeyes of ",
    "13": "12  of ",
    "14": "12.5 of ",
    "15": "Xeno of ",
    "16": "Pilot of ",
    "17": "Satellite of ",
    "18": "Queen  of ",
    "19": "King of ",
    "20": "Shkreeb of ",
    "21": "Golem of ",
    "22": "Aces (high) of ",
}   

dictOrcx = {

    "23": "Chieftain (orcx): Demands tribute from all other players--each must give one card from their hand to whoever played the Chieftain. If played together with Barney, each must give two cards from their hand to whoever played the Chieftain. If they can’t, they are eliminated from the hand." ,
    "24": "Pimp (Orcx): Each player still in the hand must take a shot. Their next bet must be made twice: the first is given directly to the pimp as a tarrif. The second is made as normal. The tariff is collected at the end of the hand by the player who played the pimp, if the pimp is still active.",
    "25": "Barney (Orcx): Spaegas rules mean Barney is painted purple (stealfy variant). Remove from the game until the final showdown: then, add to your hand as any non-wildcard. Alternatively, can counter the knight."
}

dictGuns = {

    "23": "Deathray (Guns): Select one player. If they don’t pass you a card at the next available opportunity, you may destroy 1d4 of their cards at random. If you would destroy more cards than they have in their hand, you instead eliminate them from the hand. Alternatively, destroys the pirate fleet." ,
    "24": "360 noscope (Guns): throw the card into the air. The player it lands closest to is eliminated from the hand",
    "25": "Pirate Fleet (Guns): when played, remains in the game until destroyed. At the beginning of each of your turns, you may steal one card from any other player."
}

dictSuns = {

    "23": "Napalm (Suns): Play immediately before the final showdown.  All players in the hand must vote on who eats the napalm. Majority vote wins. The player who eats the napalm is eliminated from the hand. Alternatively, destroys the pirate fleet. " ,
    "24": "Knight (Suns): when played, choose any two players. They must arm-wrestle. The winner keeps the loser’s cards! Alternatively, can counter the chieftain. ",
    "25": "SpAzathoth (Suns): Immediately destroys all cards in the game. Everyone draws a new hand of five. "
}

dictKlorxx = {

    "23": "Dr. Meebus (Klorxx): If played, Summons SpAzathoth. If in your hand, you are immune to SpAzathoth, napalm, and the deathray. " ,
    "24": "Janitor (Klorxx): Closed for cleaning! Counter one other wildcard or remove it from the game.",
    "25": "Prophecy (Klorxx): when played, choose one player and reveal their hand to the table. If there are any wildcards in their hand, add them to your hand. "
}

#-------------------------------------------------------------------------------------------------


#below are variables for the pot/betting system
mainPot = 0
sidePots = []


#-------------------------------------------------------------------------------------------------
def CardGen():
    intSuit = 0
    intNum = 0
    #zeroes out integers - I had problems with random repeating too often for my liking

    intSuit = int(random.randint(1, 4))
    intNum = int(random.randint(1, 25))
    #gets two random numbers
    #note here that randint ending bound number is exclusive
    
    OutputStr = "primary error"
    #declares output variable as "primary error" - if procesing fails it will output as such
    
    
    if intNum < 23:
        #return( + "orx"])
            OutputStr = dictCards[str(intNum)] + dictSuit[str(intSuit)]
            #if number is less than 23 (25 suit cards minus special) then print card plus random suit
    else:
            
        if intSuit == 1:
            #orcx
            OutputStr = dictOrcx[str(intNum)] 
        elif intSuit == 2:
            #guns
            OutputStr = dictGuns[str(intNum)]
        elif intSuit == 3:
            #suns
            OutputStr = dictSuns[str(intNum)]
        elif intSuit == 4:
            #klorxx
            OutputStr = dictKlorxx[str(intNum)]
      #if the number is a special card, outputs the special card based upon number and suit
    return(OutputStr)
#-------------------------------------------------------------------------------------------------


    

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
#this prints whether the bot is up and running
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity("Screaming into the void"))




@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$version'):
        await message.channel.send('1.5')

    await client.process_commands(message)
#this block is to respond to set messages - note the last line allows commands to be recieved

#----------------------------------------------------------------------------------------------


@client.command()
async def spoker(ctx):
    #generates a card based upon deck
    Card = CardGen()
    #defines variable for output
    await ctx.message.author.send(Card)
    #context message author - sends response to the message author, not channel

#----------------------------------------------------------------------------------------------

@client.command()
async def roll(ctx, rollArg):

    rollOutput = re.split('[+|-|d|D]', (rollArg.replace("-","d").replace("+","d").replace("D","d").replace("*","d")))
    #normalizes and splits data to get a possible 3-input definition

    rollOutputs = []
    sumTotal = 0
    numberRolls = int(rollOutput[0])-1
    secondOutput = ""
    #declares variables - two empty variables and one variable as number of dice to roll
    
    #for every dice wanted to roll, rolls dice
    for i in range (numberRolls):

        numberRolled = random.randint(1,int(rollOutput[1]))
        #creates and rolls based upon dice selection
        
        rollOutputs.append(numberRolled)
        #appends to rollOutputs what the roll was for integrety
        
        #print(rollOutputs) #debugger

        sumTotal = sumTotal + numberRolled
        #updates sum


    if "-" in rollArg: 
        #subtraction operator - subtracts third value, makes secondOutput reflect this
        sumTotal = sumTotal - int(rollOutput[2])
        secondOutput = " - " + str(rollOutput[2])                          

    elif "+" in rollArg: 
        #addition operator - adds third value, makes secondOutput reflect this
        sumTotal = sumTotal + int(rollOutput[2])
        secondOutput = " + " + str(rollOutput[2]) 

    elif "*" in rollArg: 
        #multiply operator - multiplies by third value, makes secondOutput reflect this
        sumTotal = sumTotal * int(rollOutput[2])
        secondOutput = " * " + str(rollOutput[2]) 

    #currently only performs one operator at a time


    await ctx.send(str(sumTotal))
    await ctx.send("(" + str(rollOutputs) + secondOutput + ")")
    #context - sends responses to channel, second displays the rolls and the operator used

#----------------------------------------------------------------------------------------------

@client.command()
async def secroll(ctx, rollArg):

    rollOutput = re.split('[+|-|d|D]', (rollArg.replace("-","d").replace("+","d").replace("D","d").replace("*","d")))
    #normalizes and splits data to get a possible 3-input definition

    rollOutputs = []
    sumTotal = 0
    numberRolls = int(rollOutput[0])
    secondOutput = ""
    #declares variables - two empty variables and one variable as number of dice to roll
    
    #for every dice wanted to roll, rolls dice
    for i in range (numberRolls):

        numberRolled = random.randint(1,int(rollOutput[1]))
        #creates and rolls based upon dice selection
        
        rollOutputs.append(numberRolled)
        #appends to rollOutputs what the roll was for integrety
        
        #print(rollOutputs) #debugger

        sumTotal = sumTotal + numberRolled
        #updates sum


    if "-" in rollArg: 
        #subtraction operator - subtracts third value, makes secondOutput reflect this
        sumTotal = sumTotal - int(rollOutput[2])
        secondOutput = " - " + str(rollOutput[2])                          

    elif "+" in rollArg: 
        #addition operator - adds third value, makes secondOutput reflect this
        sumTotal = sumTotal + int(rollOutput[2])
        secondOutput = " + " + str(rollOutput[2]) 

    elif "*" in rollArg: 
        #multiply operator - multiplies by third value, makes secondOutput reflect this
        sumTotal = sumTotal * int(rollOutput[2])
        secondOutput = " * " + str(rollOutput[2]) 

    #currently only performs one operator at a time

    # POSSIBLE ERROR IN MULTIPLICATION CHECK WITH SPLITS -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    
    await ctx.message.author.send(str(sumTotal))
    await ctx.message.author.send("(" + str(rollOutputs) + secondOutput + ")")
    #context - sends responses to message author, second displays the rolls and the operator used

#----------------------------------------------------------------------------------------------


@client.command()
async def mainpot(ctx, arg):
    global mainPot
    mainPot = mainPot + int(arg)
    #adds to main pot
    await ctx.send("current pot is: " + str(mainPot))
    
#----------------------------------------------------------------------------------------------

@client.command()
async def sidepot(ctx,arg):
    global sidePots
    global mainPot
    sidePots.append(str(mainPot) + " - " + str(arg))
    #adds current pot to side pots list as well as name of pot
    await ctx.send("current sidepots are: " + str(sidePots))

#----------------------------------------------------------------------------------------------

@client.command()
async def resetpot(ctx):
    global sidePots
    global mainPot
    sidePots = []
    mainPot = 0
    #resets main and side pots
    await ctx.send("Reset all pots")

#----------------------------------------------------------------------------------------------
@client.command()
async def allcommands(ctx):
    
    await ctx.send("- mainpot *arg* adds to main pot")
    await ctx.send("- sidepotpot *arg* crates a sidepot set to the current value of main pot with a name")
    await ctx.send("- resetpot resets all pots")
    await ctx.send("- spoker creates a card and slides it through your DMs")
    await ctx.send("- listpot resets all pots")
    await ctx.send("- roll *arg* rolls a die in the format (quantity)d(Dice)(operator) E.G. 1d10+3 - note only one operator at a time")
    await ctx.send("- secroll *arg* does the same as roll, but DM's it to you")

#----------------------------------------------------------------------------------------------
@client.command()
async def comspoker(ctx):
    
    await ctx.send("- mainpot *arg* adds to main pot")
    await ctx.send("- sidepotpot *arg* crates a sidepot set to the current value of main pot with a name")
    await ctx.send("- resetpot resets all pots")
    await ctx.send("- listpot lists all pots")
    

#----------------------------------------------------------------------------------------------
@client.command()
async def commands(ctx):
    
    await ctx.send("for list of all commands type \"allcommands\"")
    await ctx.send("for list of spoker commands type \"comspoker\"")
    

#----------------------------------------------------------------------------------------------
@client.command()
async def listpot(ctx):
    global sidePots
    global mainPot
    await ctx.send("current main pot is: " + str(mainPot))
    await ctx.send("current sidepots are: " + str(sidePots))
#----------------------------------------------------------------------------------------------
"""
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("CREATE TABLE characterLoc(character, currentRoom, movement, turnCount)")
con.close()

con = sqlite3.connect("charMovement.db")
cur = con.cursor()
cur.execute("CREATE TABLE characterLoc(character, movement)")
data = [
    ("K-Bot", "Deeper"),
    ("K-Bot", "Deeper"),
    ("Jimothy", "Deeper"),
    ("Jimothy", "Stay"),
]
cur.executemany("INSERT INTO characterLoc VALUES(?, ?)", data)
con.commit()  # Remember to commit the transaction after executing INSERT.

for row in cur.execute("SELECT character, movement FROM characterLoc WHERE character = 'Jimothy' "):

    print(row)
"""
#----------------------------------------------------------------------------------------------
@client.command()
async def move(ctx, a1, a2):

    arg1=a1.capitalize()
    arg2=a2.capitalize()
    #sanitize inputs a bit
    
    data = (arg1, arg2) #create touples
    
    print(data) #double check back-end

    cur.execute("INSERT INTO characterLoc VALUES(?, ?)", data)
    con.commit()  # Remember to commit the transaction after executing INSERT

    search = (arg1,) #sets search into touple
    if arg2 == "Deeper":
        

        i = 0
        for row in cur.execute("SELECT * FROM characterLoc WHERE character = ? AND movement = 'Deeper'", search):
           i = i + 1
           #counts rows with Deeper
           print("addition " + str(i))
            
        for row in cur.execute("SELECT * FROM characterLoc WHERE character = ? AND movement = 'Back'", search):
           i = i - 1
           #subtracts rows with Back
           print("Subtraction " + str(i))

        #prints current row
        await ctx.send(arg1 + "'s current layer is " + str(i))

#----------------------------------------------------------------------------------------------

def RowCount(searchVar):
    search = (searchVar.capitalize(),) #sets search into touple
    i = 0
    for row in cur.execute("SELECT * FROM characterLoc WHERE character = ? AND movement = 'Deeper'", search):
        i = i + 1
        #counts rows with Deeper
        print("addition " + str(i))
            
    for row in cur.execute("SELECT * FROM characterLoc WHERE character = ? AND movement = 'Back'", search):
        i = i - 1
        #subtracts rows with Back
        print("Subtraction " + str(i))
    return str(i)

            
#----------------------------------------------------------------------------------------------

@client.command()
async def deeper(ctx, a1):

    arg1=a1.capitalize()
    #sanitize input a bit
    
    data = (arg1,) #create touples
    

    cur.execute("INSERT INTO characterLoc VALUES(?, 'Deeper')", data)
    con.commit()  # Remember to commit the transaction after executing INSERT


    await ctx.send(arg1 + "'s current layer is " + RowCount(a1))

#----------------------------------------------------------------------------------------------

@client.command()
async def stay(ctx, a1):

    arg1=a1.capitalize()
    #sanitize input a bit
    
    data = (arg1,) #create touples
    

    cur.execute("INSERT INTO characterLoc VALUES(?, 'Stay')", data)
    con.commit()  # Remember to commit the transaction after executing INSERT


    await ctx.send(arg1 + "'s current layer is " + RowCount(a1))

#----------------------------------------------------------------------------------------------

@client.command()
async def back(ctx, a1):

    arg1=a1.capitalize()
    #sanitize input a bit
    
    data = (arg1,) #create touples
    

    cur.execute("INSERT INTO characterLoc VALUES(?, 'Back')", data)
    con.commit()  # Remember to commit the transaction after executing INSERT


    await ctx.send(arg1 + "'s current layer is " + RowCount(a1))

#----------------------------------------------------------------------------------------------

@client.command()
async def locations(ctx, arg1):
    print("called")
    search = (arg1,) #sets search into touple

    i = 0
    output = ("Turn - Name - Action \n")
    #await ctx.send("Turn - Name - Action")
    
    for row in cur.execute("SELECT * FROM characterLoc WHERE character = ?", search):
       i = i + 1
       output = output + (str(i) + " - " + str(row[0]) + " - " + str(row[1]) + ' \n ')
      # print(row)

    await ctx.send(output)     

       
    

#----------------------------------------------------------------------------------------------

@client.command()
async def usersetup(ctx, arg1, member: discord.Member):
    #guild is just the calling server 
    guild = ctx.message.guild
    #user: discord.PermissionOverwrite(view_channel=True)
    #declares default secret variables
    overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True),
    member: discord.PermissionOverwrite(view_channel=True)
}

    

    await ctx.guild.create_category(arg1+' character',overwrites = overwrites)
    #creates category
    
    category = discord.utils.get(guild.categories, name=str(arg1+' character'),overwrites = overwrites)
    #checks for and declares category
    
    await guild.create_text_channel(str(arg1)+'-info',overwrites = overwrites,category = category,)
    await guild.create_text_channel(str(arg1)+'-chat',overwrites = overwrites,category = category)
    await guild.create_text_channel(str(arg1)+'-rolls',overwrites = overwrites,category = category)
    #creates the three channels
   


#----------------------------------------------------------------------------------------------





client.run(TOKEN)
#starts up bot

#put command info into global dictionary, pull for each command eg (command HELP)

#put a stop command triggered via discord such that bot can be put into app format and easily shut down

#put macros in user-dependant files


