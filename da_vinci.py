import os
import discord
from discord.ext import commands
from voice_cog import VoiceCog
from channels import VoiceChannel

bot = commands.Bot(command_prefix='d$')

voice_cog = VoiceCog(bot)
bot.add_cog(voice_cog)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if after.channel.id == VoiceChannel.bathroom.value:
        print(f"{member.name} joined the bathroom")
        vc = await voice_cog.join_channel(after.channel)
        voice_cog.say_text("You look cute", vc)

@bot.command()
async def ping(ctx):
    await ctx.send("pong", tts=True)

token = os.environ.get('BOT_DA_VINCI_TOKEN')
if not token:
    print("Environment variable `BOT_DA_VINCI_TOKEN` not set")
    exit(1)

bot.run(token)
