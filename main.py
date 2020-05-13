import os
import random
import asyncio

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')


@bot.command(name="boss")
async def help_command(ctx):
    await ctx.send("Acest bot este facut de nicusor43 etc etc")


@bot.command(name="zar")
async def zar_command(ctx):
    if ctx.author == "nicusor43":
        numar = random.choice(range(3, 7))
    else:
        numar = random.choice(range(1, 7))
    await ctx.send(f'Ai dat {numar}')


@bot.command(name="greet")
async def greet_command(ctx):
    await ctx.send(f'Bine ai venit, {ctx.author}')


@bot.command(name="laba", description="Afla cine-i labagiu")
async def swear_command(ctx):
    if "nicusor43" in str(ctx.author):
        await ctx.send(f'Acest utilizator nu da laba')
    else:
        await ctx.send(f'{ctx.author} e un mare labagiu')


@bot.command(name="guess", description="Ghiceste un numar intre 1 si 100")
async def guess_command(context):
    number = random.randint(1,101)
    for guess in range(0, 5):
        await context.send('Pick a number between 1 and 100')
        msg = await client.wait_for('message', check=check)
        attempt = int(msg.content)
        if attempt > number:
            await context.send(str(guess) + ' guesses left...')
            await asyncio.sleep(1)
            await context.send('Try going lower')
            await asyncio.sleep(1)
        elif attempt < number:
            await context.send(str(guess) + ' guesses left...')
            await asyncio.sleep(1)
            await context.send('Try going higher')
            await asyncio.sleep(1)

        else:
            await context.send('You guessed it! Good job!')
            break
    else:
        await context.send("You didn't get it")

def check(message):
    try:
        int(message.content)
        return True
    except ValueError:
        return False

bot.run(TOKEN)
client.run(TOKEN)
