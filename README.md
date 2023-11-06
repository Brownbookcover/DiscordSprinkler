# Sprinkler-Bot
A Discord bot that uses a Raspberry Pi and Discord.py to be able to schedule and run a sprinkler system over the internet

After downloading code, run ```python3 -m pip install -r requirments.txt``` to download all dependencies for the code. The main two are discord.py and its dependencies and then Rpi.GPIO which is how this code interacts with the GPIO pins on the Rasberry Pi. Note: This code is runnable on a Windows computer but cannot interact with a relay board so actual sprinkler interactions are impossible unless this code is run on a Pi. 

Further Note: If you are familiar with Discord bots you know each of them require a unique bot token to run. I have not included my own token for obvious reasons so in the same directory in which you put index.py also include a token.txt file with your own unique bot token or change the last line of index.py from
```
bot.run(botToken)
```
to
```
bot.run(YourTokenHere)
```
