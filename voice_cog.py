import sys
import discord
from discord.ext import commands
from gtts import gTTS

class VoiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('Specify a channel or join one first.')

        await self.join_channel(channel, ctx.voice_client)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def say(self, ctx, *, text=None):
        if not text:
            await ctx.send("You have to tell me what to say.")
            return

        if not ctx.voice_client:
            await ctx.send("Use $join to invite me into a voice channel before you ask me to speak.")
            return

        self.say_text(text, ctx.voice_client)

    async def join_channel(self, channel: discord.VoiceChannel, vc=None):
        if vc is None:
            vc = next(iter(self.bot.voice_clients), None)

        if vc:
            if vc.channel.id == channel.id:
                return vc
            try:
                await vc.move_to(channel)
                return vc
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                return await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

    def say_text(self, text, vc):
        temp_file = "/tmp/text.mp3"
        gTTS(text=text, lang="en").save(temp_file)
        vc.play(discord.FFmpegPCMAudio(temp_file), after=lambda e: print(f"Finished playing, error: {e}"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
