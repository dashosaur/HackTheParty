import discord
from discord.ext import commands
from gtts import gTTS

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send("pong", tts=True)
    
@bot.command()
async def join(ctx, *, channel: discord.VoiceChannel=None):
    if not channel:
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise InvalidVoiceChannel('Specify a channel or join one first.')

    vc = ctx.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
    else:
        try:
            await channel.connect()
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def say(ctx, *, text=None):
    if not text:
        await ctx.send("")
        return

    vc = ctx.voice_client
    if not vc:
        await ctx.send("Use $connect to invite me into a voice channel before you ask me to speak.")
        return
    
    tts = gTTS(text=text, lang="en")
    tts.save("text.mp3")
    
    try:
        vc.play(discord.FFmpegPCMAudio('text.mp3'), after=lambda e: print(f"Finished playing, error: {e}"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
    
    except ClientException as e:
        await ctx.send(f"ClientException:\n`{e}`")
    except TypeError as e:
        await ctx.send(f"TypeError:\n`{e}`")
    except OpusNotLoaded as e:
        await ctx.send(f"OpusNotLoaded: \n`{e}`")

bot.run('ODA3ODU3NDUyNzYyMzk4NzYw.YB-F4g.O736qtzgNPCwn_5r9HxV66hjMvA')
