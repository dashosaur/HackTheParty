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
    author = message.author
    if channel.id != VoiceChannel.kates_computer.value:
        return
    if author.bot:
        return

    if '--forgot-password' in message.content:
        await channel.send('Please answer the following security question:')
        await channel.send('What is Dash\'s favorite animal?')
        msg = await bot.wait_for('message', check=lambda m: m.author == author and m.channel == channel)
        if msg.content == 'sloth':
            await channel.send('successfully logged in as Dash')
        else:
            await channel.send('login failed')
    elif message.content.startswith('login'):
        await channel.send('usage: login [-P <password>] [--forgot-password]')

@bot.command()
async def ping(ctx):
    await ctx.send("pong", tts=True)

token = os.environ.get('BOT_DA_VINCI_TOKEN')
if not token:
    print("Environment variable `BOT_DA_VINCI_TOKEN` not set")
    exit(1)

bot.run(token)
