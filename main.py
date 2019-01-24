import discord
from discord.ext import commands
import youtube_dl
import os
import json

voice_client = None

made_volume_transformer = False

is_paused = False

stopped_playing = True

song_path = "" # Path to "song.mp3". 

client = commands.Bot(command_prefix="") # Bot prefix.

@client.event
async def on_ready():
    print("Bot online.")
    print("-----------")

@client.command()
async def play(ctx, message):
    global voice_client
    global stopped_playing
    try:
        os.remove(song_path)
    except:
        pass
    if "playlist 1" in message:
        with open("playlists.json", "r") as file:
            try:
                data = json.load(file)
            except:
                data = {}
        video_link = data[str(ctx.message.author)][0]
        video_link = video_link[video_link.find("https"):]
        ydl_opts = {'outtmpl': song_path}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            video_title = info_dict.get('title', None)
        voice_client = await discord.VoiceChannel.connect(ctx.message.author.voice.channel)
        voice_client.play(discord.FFmpegPCMAudio(song_path))
        stopped_playing = False
        await ctx.send("Now playing: **{}**.".format(video_title))
    elif "playlist 2" in message:
        with open("playlists.json", "r") as file:
            try:
                data = json.load(file)
            except:
                data = {}
        video_link = data[str(ctx.message.author)][1]
        video_link = video_link[video_link.find("https"):]
        print(video_link)
        ydl_opts = {'outtmpl': song_path}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            video_title = info_dict.get('title', None)
        voice_client = await discord.VoiceChannel.connect(ctx.message.author.voice.channel)
        voice_client.play(discord.FFmpegPCMAudio(song_path))
        stopped_playing = False
        await ctx.send("Now playing: **{}**.".format(video_title))
    elif "playlist 3" in message:
        with open("playlists.json", "r") as file:
            try:
                data = json.load(file)
            except:
                data = {}
        video_link = data[str(ctx.message.author)][2]
        video_link = video_link[video_link.find("https"):]
        ydl_opts = {'outtmpl': song_path}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_link, download=True)
            video_title = info_dict.get('title', None)
        voice_client = await discord.VoiceChannel.connect(ctx.message.author.voice.channel)
        voice_client.play(discord.FFmpegPCMAudio(song_path))
        stopped_playing = False
        await ctx.send("Now playing: **{}**.".format(video_title))
    else:          
        ydl_opts = {'outtmpl': song_path,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(message, download=True)
            video_title = info_dict.get('title', None)
        try:
            voice_client = await discord.VoiceChannel.connect(ctx.message.author.voice.channel)
        except:
            pass
        voice_client.play(discord.FFmpegPCMAudio(song_path))
        stopped_playing = False
        await ctx.send("Now playing: **{}**.".format(video_title))

@client.command()
async def pause(ctx):
    global voice_client
    global is_paused
    if voice_client is None:
        await ctx.send("Audio wasn't playing.")
    elif voice_client.is_playing() is False and is_paused is False:
        await ctx.send("Audio isn't playing.")
    elif is_paused:
        await ctx.send("Audio is already paused.")
    else:
        voice_client.pause()
        is_paused = True
        await ctx.send("Paused audio.")

@client.command()
async def resume(ctx):
    global voice_client
    global is_paused
    global stopped_playing

    if is_paused:
        if stopped_playing:
            await ctx.send("Audio isn't paused.")
        else:
            voice_client.resume() 
            is_paused = False 
            await ctx.send("Resumed audio.")  
    else:
        if voice_client.is_playing():
            await ctx.send("Audio is already playing.")
        else:
            await ctx.send("Audio wasn't playing.")

@client.command()
async def volume(ctx, message=None):
    global voice_client
    global made_volume_transformer
    bad_message_type = False
    if voice_client is None:
        await ctx.send("Audio isn't playing.")
    elif voice_client.is_playing() is False:
        if is_paused:
            if message is None:
                if made_volume_transformer is True:
                    await ctx.send("The current volume is **{}**.".format(voice_client.source.volume))
                elif made_volume_transformer is False:
                    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                    made_volume_transformer = True
                    await ctx.send("The current volume is **1.0**.")
            else:
                try:
                    volume_value = float(message)
                except:
                    bad_message_type = True
                if bad_message_type:
                    await ctx.send("That is not a possible volume.")
                else:
                    if volume_value < 0:
                        await ctx.send("That volume is not possible. The range of volume is 0 to 1.5.")
                    elif volume_value > 1.5:
                        await ctx.send("That volume is too loud. The range of volume is 0 to 1.5.")
                    else:
                        if made_volume_transformer is True:
                            voice_client.source.volume = volume_value
                            await ctx.send("Changed volume to **{}**.".format(volume_value)) 
                        else:
                            voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                            made_volume_transformer = True
                            voice_client.source.volume = volume_value
                            await ctx.send("Changed volume to **{}**.".format(volume_value)) 
        else:
            await ctx.send("Audio isn't playing.")
    else:
        if message is None:
            if made_volume_transformer is True:
                await ctx.send("The current volume is **{}**.".format(voice_client.source.volume))
            elif made_volume_transformer is False:
                voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                made_volume_transformer = True
                await ctx.send("The current volume is **1.0**.")
        else:
            try:
                volume_value = float(message)
            except:
                bad_message_type = True
            if bad_message_type:
                await ctx.send("That is not a possible volume.")
            else:
                if volume_value < 0:
                    await ctx.send("That volume is not possible. The range of volume is 0 to 1.5.")
                elif volume_value > 1.5:
                    await ctx.send("That volume is too loud. The range of volume is 0 to 1.5.")
                else:
                    if made_volume_transformer is True:
                        voice_client.source.volume = volume_value
                        await ctx.send("Changed volume to **{}**.".format(volume_value)) 
                    else:
                        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                        made_volume_transformer = True
                        voice_client.source.volume = volume_value
                        await ctx.send("Changed volume to **{}**.".format(volume_value)) 

@client.command()
async def playlist(ctx, *, message=None):
    author = ctx.message.author
    with open("playlists.json", "r") as file:
        try:
            data = json.load(file)
        except:
            data = {}
    if message is None:
        if str(author) in data:
            thing1 = data[str(author)][0]
            thing2 = data[str(author)][1]
            thing3 = data[str(author)][2]
            embed = discord.Embed(
                title=author.display_name + "'s playlist:",
                color=16746496
            )
            embed.add_field(
                name="Entry 1",
                value=thing1,
                inline=False
            )
            embed.add_field(
                name="Entry 2",
                value=thing2,
                inline=False
            )
            embed.add_field(
                name="Entry 3",
                value=thing3,
                inline=False
            )
            await ctx.send(embed=embed)
        else:
            data.update({str(author): ["BLANK", "BLANK", "BLANK"]})
            embed = discord.Embed(
                title=author.display_name + "'s playlist:",
                color=16746496
            )
            embed.add_field(
                name="Entry 1",
                value="BLANK",
                inline=False
            )
            embed.add_field(
                name="Entry 2",
                value="BLANK",
                inline=False
            )
            embed.add_field(
                name="Entry 3",
                value="BLANK",
                inline=False
            )
            await ctx.send(embed=embed)
    else:
        if "edit 1 " in message:
            message = message.replace("edit 1 ", "")
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(message, download=False)
                video_title = info_dict.get("title", None)
            data[str(author)][0] = video_title + " **SOURCE**: {}".format(message)
        if "edit 2 " in message:
            message = message.replace("edit 2 ", "")
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(message, download=False)
                video_title = info_dict.get("title", None)
            data[str(author)][1] = video_title + " **SOURCE**: {}".format(message)
        if "edit 3 " in message:
            message = message.replace("edit 3 ", "")
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(message, download=False)
                video_title = info_dict.get("title", None)
            data[str(author)][2] = video_title + " **SOURCE**: {}".format(message)
    with open('playlists.json', 'w') as file:
        json.dump(data, file)

@client.command()
async def stop(ctx):
    global voice_client
    global made_volume_transformer
    global is_paused
    if voice_client.is_playing() or is_paused:
        voice_client.stop()
        made_volume_transformer = False
        is_paused = False
        stopped_playing = True
        await ctx.send("Stopped audio.")
    else:
        await ctx.send("Audio isn't playing.")

@client.command()
async def leave(ctx):
    global voice_client
    global made_volume_transformer
    global is_paused
    if voice_client is None:
        await ctx.send("Cadence is not connected to a voice channel.")
    elif voice_client.is_playing():
        await ctx.send("Please stop the music first.")
    else:
        await voice_client.disconnect()
        made_volume_transformer = False
        is_paused = False

client.run("") # Bot token.