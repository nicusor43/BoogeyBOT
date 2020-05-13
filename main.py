import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f'{client.user.name} s-a conectat la server')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Sal {member.name}, bine ai venit in server-ul meu'
    )


@client.event
async def on_message(message):
    if message.author == client.user or message.content[0] == '!':
        return

    await message.channel.send("esti smecher @nicusor43")


@bot.command(name="boss")
async def help_command(ctx):
    await ctx.send("Acest bot este facut de nicusor43 etc etc")

@bot.command(name="zar")
async def zar_command(ctx):
    if ctx.author == "nicusor43":
        numar = random.choice(range(3,7))
    else:
        numar = random.choice(range(1,7))
    await ctx.send(f'Ai dat {numar}')

@bot.command(name="greet")
async def greet_command(ctx):
    await ctx.send(f'Bine ai venit, {ctx.author}')


bot.run(TOKEN)
client.run(TOKEN)
