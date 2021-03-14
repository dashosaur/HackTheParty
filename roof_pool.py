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
    bot.noob_role = get(guild.roles, id=Role.n00b.value)
    bot.npc_role = get(guild.roles, id=Role.npc.value)
    overwrite = discord.PermissionOverwrite()
    overwrite.connect = False
    # TODO run me once
    # for vc in guild.voice_channels:
    #     if vc.id == VoiceChannel.roof_pool.value:
    #         continue
    #     await vc.set_permissions(bot.noob_role, overwrite=overwrite, reason="Roof Pool Bot")
    #     print(f'set permission for {vc}')

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot or member.has_role(bot.npc_role):
        return

    # ignore voice state changes aside from channel moves (e.g. mute / unmute)
    if before.channel == after.channel:
        return

    if after.channel is not None and after.channel.id == VoiceChannel.roof_pool.value:
        print(f"{member.name} entered the roof")
        await execute_story(member, after.channel)
    elif before.channel is not None and before.channel.id == VoiceChannel.roof_pool.value:
        print(f"{member.name} left the roof")
        await member.remove_roles(bot.noob_role)

async def execute_story(member, channel):

    if bot.is_executing_story:
        print("Ignoring request to execute since a story is already in progress")
        return
    bot.is_executing_story = True
    print("Executing story")
    party_log = await bot.get_channel(VoiceChannel.party_log.value)

    vc = await voice_cog.join_channel(channel)
    await asyncio.sleep(0.5)
    voice_cog.say_text("<speak>Hey! <break time=\"0.5s\" /> hold the door!</speak>", vc, "en-US-Wavenet-A")

    await party_log.send(f'{member.name} entered the roof, freeing the n00bs (count: {len(channel.members) - 2})')
    for channel_member in channel.members:
        if channel_member.bot or channel_member.has_role(bot.npc_role):
            continue
        print(f"Freeing {channel_member.name}")
        await channel_member.remove_roles(bot.noob_role)

    print("The n00bs are free!")

    await asyncio.sleep(4)
    print("The door shuts")

    await party_log.send(f'Trapping the n00bs (count: {len(channel.members) - 2})')
    for channel_member in channel.members:
        if channel_member.bot or channel_member.has_role(bot.npc_role):
            continue
        print(f"Assigning n00b role to {channel_member.name}")
        await channel_member.add_roles(bot.noob_role)

    if all(map(lambda m: m.bot or m.has_role(bot.npc_role), channel.members)):
        print("Skipping second message because the channel is empty")
    else:
        voice_cog.say_text("Oh no, the door shut before we could get out! We'll be locked up here until someone finds us again.", vc, "en-US-Wavenet-E")

    bot.is_executing_story = False

token = os.environ.get('BOT_ROOF_POOL_TOKEN')
if not token:
    print("Environment variable `BOT_ROOF_POOL_TOKEN` not set")
    exit(1)

bot.run(token)
