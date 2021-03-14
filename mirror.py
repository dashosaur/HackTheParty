import os
import discord
import random
import time
import sys
from discord.ext import commands
from voice_cog import VoiceCog
from channels import VoiceChannel

bot = commands.Bot(command_prefix='m$')

voice_cog = VoiceCog(bot)
bot.add_cog(voice_cog)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    # ignore voice state changes aside from channel moves (e.g. mute / unmute)
    if before.channel == after.channel:
        return

    print(f"{member.name} moved from {before.channel.name if before.channel else None} to {after.channel.name if after.channel else None}")

    channel_id = VoiceChannel.school_bathroom.value if len(sys.argv) > 1 else VoiceChannel.cyberdelia_bathroom.value

    if before.channel and before.channel.id == channel_id:
        print(f"{member.name} left the bathroom")
        # if all real users have left, the bot should leave too
        if all(map(lambda m: m.bot, before.channel.members)):
            print(f"The bathroom is empty, leaving")
            await voice_cog.leave_channel()

    if after.channel and after.channel.id == channel_id:
        print(f"{member.name} entered the bathroom")

        time.sleep(.5)
        vc = await voice_cog.join_channel(after.channel)
        compliments = clean_compliments if len(sys.argv) > 1 else dirty_compliments
        text = random.choice(compliments).replace("{name}", member.nick or member.name or "Babe")
        voice_cog.say_text(text, vc)
        await party_log.send(f'Mirror to {member.name}: {text}')

clean_compliments = [
    "{name}, you look slick all day",
    "Yo... you kinda look like a god",
    "{name}, you're elite",
    "Is your name Wi-fi? Because I'm really feeling a connection.",
    "Hey {name}, you had me at Hello World.",
    "You look good in a dress",
    "Baby, if they made you in C, you would have a pointer to my heart. If they made you in Java, you'd be the object of my desire.",
    "Hey {name}, can you be my private variable? I want to be the only one with access to you.",
    "Hey {name}, are you airdropping me something? Because I’m really feeling a connection",
    "Hey {name}, are you a double? The thought of you always floats inside my head",
    "Hey {name}, are you an exception? Let me catch you",
    "Hey cutie, if you were a part of my domain, we could share cookies.",
]

dirty_compliments = [
    "Now I'm trying to save you from yourself but you gotta stop letting your mama dress you, man!",
    "Your only crime is that of curiosity",
    "Hey {name}, you make my software turn into hardware",
    "What's your interest in me? Academic, purely sexual, or homicidal?",
    "Hey babe, if you have an empty slot, I have the card to fill it.",
    "Hey babe, your homepage or mine?",
    "Spandex is a privilege, not a right",
    "The pool on the roof must have a leak because I'm all wet.",
    "Hey babe, I would love to stick my pins into your sockets.",
    "Hey baby, my servers never go down... but I do!",
    "{name}, you are hotter than the bottom of my laptop",
    "Hey baby, want to experience a backdoor Trojan?",
    "Hey baby, can I do a penetration test on your back door?",
    "<speak>Hey babe, give me your number... <break time=\"1.5s\"/> sudo give me your number</speak>",
]

token_name = 'BOT_CLEAN_MIRROR_TOKEN' if len(sys.argv) > 1 else 'BOT_MIRROR_TOKEN'
token = os.environ.get(token_name)
if not token:
    print(f'Environment variable {token_name} not set')
    exit(1)

bot.run(token)
