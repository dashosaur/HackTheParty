import os
import discord
import time
from discord.ext import commands
from channels import VoiceChannel
from voice_cog import VoiceCog

bot = commands.Bot(command_prefix='i$')

voice_cog = VoiceCog(bot)
bot.add_cog(voice_cog)

@bot.event
async def on_ready():
    print('Intercom bot logged in as {0.user}'.format(bot))

@bot.command()
@commands.has_role('Broadcaster')
async def broadcast(ctx, *, text=None):
    if not text:
        await ctx.send("You have to tell me what to broadcast.")
        return

    print(f'broadcasting {text}')
    guild = bot.get_guild(802727441646092288)
    for c in guild.voice_channels:
        if not c.voice_states:
            print(f'skipping {c.name} because it\'s empty')
            continue
        print(f'joining {c.name}')
        vc = await voice_cog.join_channel(c)
        if text == 'htp':
            print(f'playing {text}x3')
            voice_cog.play_mp3('htp.mp3', vc)
            voice_cog.play_mp3('htp.mp3', vc)
            voice_cog.play_mp3('htp.mp3', vc)
        else:
            print(f'saying {text}')
            voice_cog.play_mp3('intercom-in.mp3', vc)
            voice_cog.say_text(text, vc, use_cache=True)
            voice_cog.play_mp3('intercom-out.mp3', vc)
        await vc.disconnect()

token = os.environ.get('BOT_INTERCOM_TOKEN')
if not token:
    print("Environment variable `BOT_INTERCOM_TOKEN` not set")
    exit(1)

bot.run(token)
