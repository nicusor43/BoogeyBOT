import os
import random
import asyncio

import discord
from dotenv import load_dotenv
from discord.ext import commands

from google_images_download import google_images_download

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
    number = random.randint(1, 101)
    for guess in range(0, 5):
        await context.send('Pick a number between 1 and 100')
        msg = await client.wait_for('Message')
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


@bot.command()
async def fight(ctx, member: discord.Member):
    nr = random.randint(1, 3)
    if nr == 1:
        await ctx.send(f'{ctx.author} l a batut pe {member}')
    else:
        await ctx.send(f'{member} l a batut pe {ctx.author}')


@bot.command()
async def say(ctx, *, msg: str):
    await ctx.send(msg)


@bot.command()
async def img(ctx, name: str):
    response = google_images_download.googleimagesdownload()

    arguments = {'keywords': name, 'limit': 1, "print_urls": True}
    paths = response.download(arguments)
    print(paths[0][name][0])

    file = discord.File(paths[0][name][0], filename=paths[0][name][0])
    await ctx.send(name, file=file)
    os.remove(paths[0][name][0])
    os.remove('downloads')



def check(message):
    try:
        int(message.content)
        return True
    except ValueError:
        return False


bot.run(TOKEN)
