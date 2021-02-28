import os
import discord
from discord.ext import commands
from discord.utils import get
from voice_cog import VoiceCog
from channels import VoiceChannel
from roles import Role
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='p$', intents=intents)
bot.is_executing_story = False

voice_cog = VoiceCog(bot)
bot.add_cog(voice_cog)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    roof_pool = bot.get_channel(VoiceChannel.roof_pool.value)

    guild = bot.get_guild(802727441646092288)
    noob_role = get(guild.roles, id=Role.n00b.value)
    overwrite = discord.PermissionOverwrite()
    overwrite.connect = False
    for vc in guild.voice_channels:
        if vc.id == VoiceChannel.roof_pool.value:
            continue
        # await vc.set_permissions(noob_role, overwrite=overwrite, reason="Roof Pool Bot")
        # print(f'set permission for {vc}')

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return
    if after.channel is None:
        return

    # ignore voice state changes aside from channel moves (e.g. mute / unmute)
    if before.channel == after.channel:
        return

    if after.channel.id == VoiceChannel.roof_pool.value:
        print(f"{member.name} entered the roof")
        await execute_story(member, after.channel)

async def execute_story(member, channel):
    if bot.is_executing_story:
        print("Ignoring request to execute since a story is already in progress")
        return
    bot.is_executing_story = True

    print("Saying hold the door")
    vc = await voice_cog.join_channel(channel)
    voice_cog.say_text("Hey! hold the door!", vc, "en-US-Wavenet-A")

    n00b = get(member.guild.roles, id=Role.n00b.value)

    for channel_member in channel.members:
        if channel_member.bot:
            continue
        print(f"Freeing {channel_member.name}")
        await channel_member.remove_roles(n00b)

    print("The n00bs are free!")

    await asyncio.sleep(4)
    print("The door shuts")

    channel = member.guild.get_channel(channel.id) # refetch the channel
    for channel_member in channel.members:
        if channel_member.bot:
            continue
        print(f"Assigning n00b role to {channel_member.name}")
        await channel_member.add_roles(n00b)

    voice_cog.say_text("<speak>Oh no, it shut before we could get out! We'll be locked up here until someone finds us again.</speak>", vc, "en-US-Wavenet-E")

    bot.is_executing_story = False

token = os.environ.get('BOT_ROOF_POOL_TOKEN')
if not token:
    print("Environment variable `BOT_ROOF_POOL_TOKEN` not set")
    exit(1)

bot.run(token)
