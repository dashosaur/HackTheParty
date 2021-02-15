import sys
import discord
from discord.ext import commands
from google.cloud import texttospeech
from pathlib import Path
import hashlib

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
        use_fancy_voice = True

        # md5 hash the text to get a unique enough filename
        temp_file_path = f"/tmp/bot_{hashlib.md5(text.encode()).hexdigest()}_{use_fancy_voice}.mp3"

        file = Path(temp_file_path)
        if not file.is_file():
            # generate new audio
            if not use_fancy_voice:
                gTTS(text=text, lang="en").save(temp_file_path)
            else:
                client = texttospeech.TextToSpeechClient()
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    name="en-US-Wavenet-C",
                    # ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )
                response = client.synthesize_speech(
                    input=texttospeech.SynthesisInput(text=text),
                    voice=voice,
                    audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
                )
                with open(temp_file_path, "wb") as out:
                    out.write(response.audio_content)

        vc.play(discord.FFmpegPCMAudio(temp_file_path), after=lambda e: print(f"Finished playing, error: {e}"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 1
