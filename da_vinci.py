from channels import VoiceChannel
from discord.ext import commands
from hack_points import award_hack_points
import asyncio
import discord
import os
import random
import re
import uuid

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='d$', intents=intents)

def sanitize(str):
    return re.sub(r'[^a-z ]','',str.lower())

def sanitize_key(str):
    ret = re.sub(r'[^a-z ]','', str.lower())
    return re.sub(' ','_', ret)

@bot.event
async def on_ready():
    print('Da Vinci bot logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    #TODO test me
    await greet_member_with_questions(member)

async def greet_member_with_questions(member):
    def check(m):
        print(f'author matches: {m.author == member}, isinstance:{isinstance(m.channel, discord.channel.DMChannel)}')
        return m.author == member and isinstance(m.channel, discord.channel.DMChannel)

    await member.send('Welcome to Dusty and Bryan\'s Birthday Party! I\'m going to ask you a few questions you can answer if you want to play a little game tonight. (Please answer with simple, succint answers; I\'m a bot from the 90\'s and not very smart.)')
    await member.send('What is your favorite animal?')
    animal = sanitize((await bot.wait_for('message', check=check)).content)
    await member.send('What color underwear are you wearing?')
    color = sanitize((await bot.wait_for('message', check=check)).content)
    await member.send('What activity has helped you most during the pandemic?')
    activity = sanitize((await bot.wait_for('message', check=check)).content)
    await member.send('Noted. Now go back to the party: https://discord.gg/UH3TQwhuJ2')

    print(f'member id: {member.id}, animal: {animal}, color: {color}, activity: {activity}')
    computer_log = bot.get_channel(VoiceChannel.kates_computer_log.value)
    await computer_log.send(f'{member.id},{animal},{color},{activity}')

    party_log = bot.get_channel(VoiceChannel.party_log.value)
    await party_log.send(f'{member.name} joined and got sent questions')

class SecurityQuestionModel:
    def __init__(self, comma_string):
        list = comma_string.content.split(',')
        self.member_id = list[0]
        self.animal = list[1]
        self.color = list[2]
        self.activity = list[3]

    def name(self, guild):
        m = guild.get_member(int(self.member_id))
        name = m.nick or m.name
        return name.split(' ')[0]

async def award_da_vinci_hack_points(hacker_snowflake, victim_snowflake):
    namespace = uuid.UUID('{f45d8434-9670-48bd-afc7-6fb2c78ceea3}')
    award_uuid = uuid.uuid5(namespace, f"{hacker_snowflake}.{victim_snowflake}")
    await award_hack_points(hacker_snowflake, 'Password Recovery', 1, award_uuid, 'da_vinci')

@bot.event
async def on_message(message):
    party_log = bot.get_channel(VoiceChannel.party_log.value)
    channel = message.channel
    author = message.author
    guild = bot.get_guild(802727441646092288)
    if channel.id != VoiceChannel.kates_computer.value:
        return
    if author.bot:
        return

    async def security_question_models():
        messages = await bot.get_channel(VoiceChannel.kates_computer_log.value).history(limit=200).flatten()

        def validate(model):
            if int(model.member_id) == author.id:
                return False
            member = guild.get_member(int(model.member_id))
            if member is None:
                return False
            if member.voice is None:
                return False
            return True

        models = list(map(lambda m: SecurityQuestionModel(m), messages))
        valid_models = filter(validate, models)
        return valid_models

    async def print_usage():
        await channel.send('usage: login <username> (--password <password> | --forgot-password)')
        models = await security_question_models()
        await channel.send(f'users: {", ".join(map(lambda m: m.name(guild), models))}')

    async def print_failed():
        await channel.send('login failed')

    async def question_flow(model, q_index=random.randint(0, 3)):
        name = model.name(guild)
        await party_log.send(f'{author.name} attempted to login as {name}')
        if q_index == 0:
            q = f'what is {name}\'s favorite animal?'
            a = model.animal
        elif q_index == 1:
            q = f'what color underwear is {name} wearing?'
            a = model.color
        else:
            q = f'what activity has kept {name} sane during the pandemic?'
            a = model.activity
        await channel.send(f'{author.mention}, answer the following security question: {q}')
        msg = await bot.wait_for('message', check=lambda m: m.author == author and m.channel == channel)
        await msg.delete()
        redacted = '•' * len(msg.content)
        await channel.send(f'{author.nick or author.name} typed: {redacted}')
        if sanitize(msg.content) == a:
            await channel.send(f'successfully logged in as {name}')
            await party_log.send(f'{author.name} successfully logged in as {name}')
            await award_da_vinci_hack_points(author.id, model.member_id)
            msg_desktop = await channel.send(embed=discord.Embed(title=f'{name.capitalize()}\'s Desktop', description='There\'s not much here.. just a game to play. You will be logged out in 10s.', url='https://www.goodoldtetris.com'));
            await asyncio.sleep(10)
            await msg_desktop.edit(content=f'{name} logged out due to inactivity', embed=None)
        else:
            await print_failed()

    if '$purge' == message.content:
        await channel.purge()
        await channel.send('this computer belongs to kate, but is shared with all her friends. no one is logged in right now.')
    elif '--register' in message.content:
        await greet_member_with_questions(author)
    elif message.content.startswith('login'):
        if '--password' in message.content:
            await print_failed()
        elif '--forgot-password' in message.content:
            # random.choice(await security_question_models())
            username = message.content.split(' ')[1]
            models = await security_question_models()
            m = next((m for m in models if m.name(guild) == username), None)
            if m:
                await question_flow(m)
            else:
                await print_usage()
        else:
            await print_usage()

token = os.environ.get('BOT_DA_VINCI_TOKEN')
if not token:
    print("Environment variable `BOT_DA_VINCI_TOKEN` not set")
    exit(1)

bot.run(token)
