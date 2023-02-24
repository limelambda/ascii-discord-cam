import discord
from discord.ext import commands
import time
from PIL import Image
import asciicam

CONFIG = open('config.txt', 'rt')

TOKEN = CONFIG.readline().split(' ')[2:][0][:-1] #Get thing after the space after = on line 1 but not the new line charecter
TIMEOUT = 5

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Logged in!')

@bot.command(name="asciicam")
async def badapple(ctx):
    oldTimestamp = time.time()
    i = 0
    while True:
        newTimestamp = time.time()
        if (newTimestamp - oldTimestamp) >= TIMEOUT:
            await ctx.message.channel.send(asciicam.getAsciiFrame())
            print('frame delivered! :3')
            newTimestamp = time.time()
            i += (newTimestamp - oldTimestamp)/TIMEOUT
            oldTimestamp = newTimestamp

bot.run(TOKEN)