import asyncio
import os
import random

import discord
import youtube_dl
from discord.ext import commands
from discord.ext.commands import has_permissions
from bing_image_downloader import downloader
from gtts import gTTS
from googletrans import Translator

# Has nothing to do with a dotenv but oh well
file = open('dotenv',mode='r')
 
TOKEN = file.read()
 
file.close()


client = discord.Client()

bot = commands.Bot(command_prefix='!')

ytdl_format_options = {
    'format': 'bestaudio/   best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,  
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'skip_download': True,
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


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
    for guess in range(0, 6):
        await context.send('Pick a number between 1 and 100')
        msg = await bot.wait_for('Message')
        attempt = int(msg.content)
        if attempt > number:
            await context.send(str(5 - guess) + ' guesses left...')
            await asyncio.sleep(1)
            await context.send('Try going lower')
            await asyncio.sleep(1)
        elif attempt < number:
            await context.send(str(5 - guess) + ' guesses left...')
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
async def img(ctx, nr: int, *, name: str,):
    if nr > 10:
        await ctx.send("Da mi ssd u tau daca esti asa smecher 1000 de poze nu vrei?")
    else:
        downloader.download(name, nr, output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60)
        for file in os.listdir(f'dataset/{name}/'):
            filename_str = f'dataset/{name}/{os.fsdecode(file)}'
            file = discord.File(filename_str, filename = filename_str)
            await ctx.send(file=file)
            os.remove(filename_str)


@bot.command()
@has_permissions(administrator=True)
async def delete(ctx, nr: int):
    await ctx.channel.purge(limit=nr)
    msg = await ctx.send(f"am sters {nr} mesaje")
    await asyncio.sleep(4)
    await msg.delete()


'''
@bot.command()
async def poll(ctx,*, q: str):
    await ctx.send("Zi ce raspunsuri vrei")
    msg = await bot.wait_for('Message')
    msg = str(msg.content).strip(" ")
    sub_poll = strawpoll.Poll(title=q, options=msg)
    api = strawpoll.API()
    await api.submit_poll(poll=sub_poll)
'''


@bot.command()
@has_permissions(administrator=True)
async def ban(ctx, member: discord.User = None, reason=None):
    if member is None or member is ctx.message.author:
        await ctx.channel.send("Nu poti sa ti dai ban singur")
        return
    if reason is None:
        reason = "Esti naspa"
    message = f"Ai fost banat {ctx.guild.name} pentru {reason}"
    await member.send(message)
    await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"{member} e banat!")


@bot.command()
@has_permissions(administrator=True)
async def unban(ctx, *, user=None):
    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        await ctx.send("Error: Nu a putut fi gasit")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Moderatorul care a fct smecheria: " + str(ctx.author))
        else:
            await ctx.send("Utilizatorul nu era banat")
            return

    except discord.Forbidden:
        await ctx.send("I do not have permission to unban!")
        return

    except:
        await ctx.send("fail")
        return

    await ctx.send(f"l am unbanat cu succes pe {user.mention}!")


@bot.command()
async def translate(ctx, source: str, destination: str, *, string: str):
    translator = Translator()
    answer = translator.translate(string, dest=destination, src=source)
    await ctx.send(answer.text)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def t2s(self, ctx, language, *, string: str):
        for item in os.listdir():
            if item.endswith('.mp3'):
                os.remove(item)
        audio = gTTS(text=string, lang=language, slow=False)
        audio.save(f"temporar.mp3")
        # ctx.voice_client.play(f"{string}.mp3")
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"temporar.mp3"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @t2s.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
            for item in os.listdir():
                if item.endswith('.webm'):
                    os.remove(item)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            for item in os.listdir():
                if item.endswith('.webm'):
                    os.remove(item)


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


def check(message):
    try:
        int(message.content)
        return True
    except ValueError:
        return False


bot.add_cog(Music(bot))
bot.run(TOKEN)
