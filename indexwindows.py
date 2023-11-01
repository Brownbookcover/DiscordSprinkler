#import RPi.GPIO as GPIO
import time as timeforsleeps
import discord
from discord.ext import commands, tasks
import datetime
#from datetime import datetime, time, timedelta
#import asyncio

description='I run some sprinklers'

in1 = 7
in2 = 11
in3 = 13

est=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
timeforscedule = datetime.time(hour=3, tzinfo=est)
listoftimes =list()
listoftimes.append(datetime.time(hour=1, minute=0, tzinfo=est))    #This cant be empty or it thorws an error so making it before the scedule run should be fine
listofallinfo = list()
listofallinfo.append([1, 0, 0])

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='~', description=description, intents=intents, case_insensitive=True)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    sceduler.start()
    dailyloop.start()

@tasks.loop(time=timeforscedule)
async def sceduler():
    channel = bot.get_channel(1164845979879624726)
    day = datetime.date.weekday(datetime.datetime.now())
    listoftimes.clear()
    listofallinfo.clear()
    file1 = open('days/'+str(day)+'.txt', 'r')
    Lines = file1.read().splitlines()
    if len(Lines)!=0:
        await channel.send("Todays sceduled runs are...")
    for line in Lines:
        timeofday, zone, length = line.split()
        await channel.send(timeofday+":00 : Zone "+zone+" for "+length+" minutes")
        listoftimes.append(datetime.time(hour=int(timeofday), tzinfo=est))
        listofallinfo.append([timeofday, zone, length])
    print(listoftimes)
    print(listofallinfo)

@tasks.loop(minutes=1)
async def dailyloop():
    channel = bot.get_channel(1164845979879624726)
    today = datetime.datetime.now()
    hour=today.hour
    minute=today.minute
    boolean = True
    for i in range(len(listofallinfo)):
        if int(listofallinfo[i][0])==hour and minute==0:
            await channel.send("Running zone "+listofallinfo[i][1]+" for "+listofallinfo[i][2]+ " mins")
            sleeptime = int(listofallinfo[i][2])
            if(int(listofallinfo[i][1]==0)):
                boolean = False
            if(int(listofallinfo[i][1])==1):
                await channel.send("Turning on 1")
                timeforsleeps.sleep(sleeptime)
                await channel.send("Turning off 1")
                boolean = False
            if(int(listofallinfo[i][1])==2):
                await channel.send("Turning on 2")
                timeforsleeps.sleep(sleeptime)
                await channel.send("Turning off 2")
                boolean = False
            if(int(listofallinfo[i][1])==3):
                await channel.send("Turning on 3")
                timeforsleeps.sleep(sleeptime)
                await channel.send("Turning off 3")
                boolean = False
            if(boolean):
                await channel.send("Not a valid zone")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def on(ctx, zone: int=0, sleeptime: int=0):
    if(zone!=0 and sleeptime!=0):
        await ctx.send('Turning on zone '+str(zone)+" for "+str(sleeptime)+" mins")
        if(zone==1):
            await ctx.send("Turning on 1")
            timeforsleeps.sleep(sleeptime)
            await ctx.send("Turning off 1")
        if(zone==2):
            await ctx.send("Turning on 2")
            timeforsleeps.sleep(sleeptime)
            await ctx.send("Turning off 2")
        if(zone==3):
            await ctx.send("Turning on 3")
            timeforsleeps.sleep(sleeptime)
            await ctx.send("Turning off 3")
    else:
        await ctx.send('Please use two numbers Usage: ~on ZONE TIME')

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

bot.run('MTE2NDg0NzQzMjkyOTEyODUwOA.GjJ7Gn.pmBO2bkXNlZlNRiVns5Mi-U6YOPgaS_X5A5rR4')