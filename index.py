import RPi.GPIO as GPIO
import time as timeforsleeps
import discord
from discord.ext import commands, tasks
import datetime
#from datetime import datetime, time, timedelta
#import asyncio

file = open('../token.txt', 'r')
botToken = file.read()
botToken = str(botToken)
description='I run some sprinklers'

in1 = 7
in2 = 11
in3 = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)

GPIO.output(in1, False)
GPIO.output(in2, False)
GPIO.output(in3, False)

est=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
timeforscedule = datetime.time(hour=1, minute=34, tzinfo=est)
listoftimes =list()
listoftimes.append(datetime.time(hour=1, minute=0, tzinfo=est))    #This cant be empty or it thorws an error so making it before the scedule run should be fine
listofallinfo = list()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='~', description=description, intents=intents, case_insensitive=True)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    send_message.start()
    dailyloop.start()
    #bot.loop.create_task(background_task())

@tasks.loop(time=timeforscedule)
async def send_message():
    channel = bot.get_channel(1164845979879624726)
    day = datetime.date.weekday(datetime.datetime.now())
    listoftimes.clear()
    listofallinfo.clear()
    file1 = open('days/'+str(day)+'.txt', 'r')
    Lines = file1.read().splitlines()
    await channel.send("Todays sceduled runs are...")
    for line in Lines:
        timeofday, zone, length = line.split()
        await channel.send(timeofday+":00 : Zone "+zone+" for "+length+" minutes")
        listoftimes.append(datetime.time(hour=int(timeofday), tzinfo=est))
        listofallinfo.append([timeofday, zone, length])
    #await channel.send(Lines)
    #await channel.send("Test")
    await channel.send(listoftimes)
    await channel.send(listofallinfo)

@tasks.loop(time=listoftimes)
async def dailyloop():
    channel = bot.get_channel(1164845979879624726)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    today = datetime.datetime.now()
    hour=today.hour
    boolean = True
    for i in (0, len(listofallinfo)):
        if int(listofallinfo[i][0])==hour:
            await channel.send("Running zone "+listofallinfo[i][1]+" for "+listofallinfo[i][2]+ "mins")
            sleeptime = int(listofallinfo[i][2])
            if(int(listofallinfo[i][1])==1):
                GPIO.output(in1, True)
                timeforsleeps.sleep(sleeptime)
                GPIO.output(in1, False)
                boolean = False
            if(int(listofallinfo[i][1])==2):
                GPIO.output(in2, True)
                timeforsleeps.sleep(sleeptime)
                GPIO.output(in2, False)
                boolean = False
            if(int(listofallinfo[i][1])==3):
                GPIO.output(in3, True)
                timeforsleeps.sleep(sleeptime)
                GPIO.output(in3, False)
                boolean = False
            if(boolean):
                await channel.send("Not a valid zone")


    GPIO.cleanup()

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def on(ctx, zone: int=0, sleeptime: int=0):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    if(zone!=0 and sleeptime!=0):
        await ctx.send('Turning on zone '+str(zone)+" for "+str(sleeptime)+" mins")
        if(zone==1):
            GPIO.output(in1, True)
            timeforsleeps.sleep(sleeptime)
            GPIO.output(in1, False)
        if(zone==2):
            GPIO.output(in2, True)
            timeforsleeps.sleep(sleeptime)
            GPIO.output(in2, False)
        if(zone==3):
            GPIO.output(in3, True)
            timeforsleeps.sleep(sleeptime)
            GPIO.output(in3, False)
    else:
        await ctx.send('Please use two numbers Usage: ~on ZONE TIME')
    GPIO.cleanup()

@bot.command()
async def add(ctx, day: int=7, hour: int=0, zone: int=0, minutes: int=0):
    check = True
    if hour>0 and hour<24 and zone>0 and minutes>0 and day>=0 and day<7:
        file1 = open('days/'+str(day)+'.txt', 'r')
        Lines = file1.read().splitlines()
        file1 = open('days/'+str(day)+'.txt', 'w')
        for line in Lines:
            file1.write(str(line)+"\n")
            if str(line)==(str(hour)+" "+str(zone)+" "+str(minutes)):
                check=False
                await ctx.send('Time already in listing not adding it')
        if check==True:
            file1.write(str(hour)+" "+str(zone)+" "+str(minutes))
    else:
        await ctx.send('Please enter 3 numbers Usage: ~add hours(0-23) zone(1+), time(1+)')

@bot.command()
async def list(ctx, day: int=7):
    if day>=0 and day<7:
        file1 = open('days/'+str(day)+'.txt', 'r')
        Lines = file1.read().splitlines()
        for number, line in enumerate(Lines):
            timeofday, zone, length = line.split()
            await ctx.send("Number "+str(number+1)+": \n \t Time: "+timeofday+":00 \n \t Zone: "+zone+" \n \t Length: "+length+ " minutes")
    else:
        await ctx.send('Please enter 1 number Usage: ~list day(0-6 0=Monday 6=Sunday)')

@bot.command()
async def delete(ctx, day: int=7, number: int=-2):
    check = True
    if number>=-1 and day>=0 and day<7:
        file1 = open('days/'+str(day)+'.txt', 'r')
        Lines = file1.read().splitlines()
        file1 = open('days/'+str(day)+'.txt', 'w')
        for numberfordelete, line in enumerate(Lines):
            if number-1!=numberfordelete:
                file1.write(str(line)+"\n")
            else:
                check = False
                timeofday, zone, length = line.split()
                await ctx.send("Deleting "+str(number)+": \n \t Time: "+timeofday+":00 \n \t Zone: "+zone+" \n \t Length: "+length+ " minutes")
        if check == True:
            await ctx.send("Nothing was deleted please make sure you have the right day or number Usage: ~delete day(0-6 0=Monday 6=Sunday) number(which line to delete please view ~list to see the options for a day)")
    else:
        await ctx.send('Please enter 2 numbers Usage: ~delete day(0-6 0=Monday 6=Sunday) number(which line to delete please view ~list to see the options for a day)')

@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Use ~help [commands] for more information about each command", color = ctx.author.color)
    em.add_field(name= "commands", value="ping,on,add,list,delete")
    await ctx.send(embed=em)

@help.command()
async def ping(ctx):
    em = discord.Embed(title = "Ping", description = "Checks if the bot is online", color = ctx.author.color)
    em.add_field(name= "**Syntax**", value="~ping")
    await ctx.send(embed=em)

@help.command()
async def on(ctx):
    em = discord.Embed(title = "On", description = "Turns on a specified zone for x minutes", color = ctx.author.color)
    em.add_field(name= "**Syntax**", value="~on zone time")
    await ctx.send(embed=em)

@help.command()
async def add(ctx):
    em = discord.Embed(title = "Add", description = "Adds a sceduled time to a certain day", color = ctx.author.color)
    em.add_field(name= "**Syntax**", value="~add day time zone length - day(0-6 0=Monday 6=Sunday) and time(0-23)")
    await ctx.send(embed=em)

@help.command()
async def list(ctx):
    em = discord.Embed(title = "List", description = "Lists all sceduled runs for that day", color = ctx.author.color)
    em.add_field(name= "**Syntax**", value="~list day - day(0-6 0=Monday 6=Sunday)")
    await ctx.send(embed=em)

@help.command()
async def delete(ctx):
    em = discord.Embed(title = "Delete", description = "Deletes a sceduled run on a certain day", color = ctx.author.color)
    em.add_field(name= "**Syntax**", value="~delete day number - day(0-6 0=Monday 6=Sunday), look at ~list to know the number to delete")
    await ctx.send(embed=em)

bot.run(botToken)