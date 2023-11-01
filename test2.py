import discord
from discord.ext import commands, tasks
import datetime
import asyncio

file = open('../token.txt', 'r')
botToken = file.read()
botToken = str(botToken)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# List to store datetimes defined in task_one
datetime_list = []


@tasks.loop(seconds=10)
async def task_one():
    # Define datetimes and add them to the datetime_list
    now = datetime.datetime.now(datetime.timezone.utc).astimezone()
    datetime_list.append(now)
    print(f"Defined datetime: {now}")

@tasks.loop(seconds=5)
async def task_two():
    # Check if there are datetimes in the list and perform actions
    if datetime_list:
        defined_datetime = datetime_list.pop(0)
        current_datetime = datetime.datetime.now(datetime.timezone.utc).astimezone()

        # Compare the defined datetime with the current datetime
        time_difference = current_datetime - defined_datetime

        # If the difference is greater than or equal to 10 seconds, perform an action
        if time_difference.total_seconds() >= 10:
            print(f"Action performed at {current_datetime}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    # Start task_one and task_two when the bot is ready
    task_one.start()
    task_two.start()

bot.run('MTE2NDg0NzQzMjkyOTEyODUwOA.GjJ7Gn.pmBO2bkXNlZlNRiVns5Mi-U6YOPgaS_X5A5rR4')