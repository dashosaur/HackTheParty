import os
import discord
from discord.ext import commands
from channels import VoiceChannel

bot = commands.Bot(command_prefix='d$')

@bot.event
async def on_ready():
    print('Da Vinci bot logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    channel = message.channel
    if channel.id != VoiceChannel.kates_computer.value:
        return
    
    if message.content.startswith('login'):
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await bot.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))

@bot.command()
async def ping(ctx):
    await ctx.send("pong", tts=True)

token = os.environ.get('BOT_DA_VINCI_TOKEN')
if not token:
    print("Environment variable `BOT_DA_VINCI_TOKEN` not set")
    exit(1)

bot.run(token)
