import os
import discord
from discord.ext import commands
from discord.utils import get
from voice_cog import VoiceCog
from channels import VoiceChannel
from roles import Role
import time

bot = commands.Bot(command_prefix='p$')

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

    if after.channel.id == VoiceChannel.roof_pool.value:
        print(f"{member.name} entered the roof")

        print("Saying hold the door")
        vc = await voice_cog.join_channel(after.channel)
        voice_cog.say_text("<speak>Hey! <break time=\"1s\" /> hold the door!</speak>", vc, "en-US-Wavenet-A")

        n00b = get(member.guild.roles, id=Role.n00b.value)

        for channel_member in after.channel.members:
            if channel_member.bot:
                continue
            print(f"Freeing {channel_member.name}")
            await channel_member.remove_roles(n00b)
        print("The n00bs are free!")

        time.sleep(4)
        print("The door shuts")
        for member_id in after.channel.voice_states.keys():
            await member.add_roles(n00b)

        voice_cog.say_text("<speak>Oh no, it shut before we could get out! We'll be locked up here until someone finds us again.</speak>", vc, "en-US-Wavenet-E")

token = os.environ.get('BOT_ROOF_POOL_TOKEN')
if not token:
    print("Environment variable `BOT_ROOF_POOL_TOKEN` not set")
    exit(1)

bot.run(token)
