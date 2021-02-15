import os
import discord
from discord.ext import commands
from voice_cog import VoiceCog

bot = commands.Bot(command_prefix='$')

voice_cog = VoiceCog(bot)
bot.add_cog(voice_cog)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if after.channel.id == 807845575730659348:
        print(f"{member.name} joined the bathroom")
        vc = await after.channel.connect()
        voice_cog.say_text("You look cute", vc)

@bot.command()
async def ping(ctx):
    await ctx.send("pong", tts=True)

token = os.environ.get('BOT_TOKEN')
if not token:
    print("Environment variable `BOT_TOKEN` not set")
    exit(1)

bot.run(token)
