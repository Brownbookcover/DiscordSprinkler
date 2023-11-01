#import RPi.GPIO as GPIO
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

est=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
timeforscedule = datetime.time(hour=22, minute=8, second=0, tzinfo=est)
listoftimes =list()
listoftimes.append(datetime.time(hour=22, minute=8, second=10))
listoftimes.append(datetime.time(hour=22, minute=8, second=20))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='~', description=description, intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    sceduler.start()
    dailyloop.start()

@tasks.loop(time=timeforscedule)
async def sceduler():
    listoftimes.append(datetime.time(hour=22, minute=8, second=30))
    listoftimes.append(datetime.time(hour=22, minute=8, second=40))
    print(listoftimes)

@tasks.loop(seconds=1)
async def dailyloop():
    print(datetime.datetime.now().time().replace(microsecond=0))
    if datetime.datetime.now().time().replace(microsecond=0) in listoftimes:
        channel = bot.get_channel(1164845979879624726)
        await channel.send("I got here")

bot.run(botToken)