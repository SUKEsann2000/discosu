import discord
import requests
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
import os

import json
import osu


TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    """
    channel = client.get_channel(1133921658500026480)

    
    token = await get_osu_token()
    beatmap = await get_daily_beatmap(token)

    fp = open("beatmap.json", "w", encoding="utf-8")
    json.dump(beatmap, fp, ensure_ascii=False, indent=4)
    fp.close()

    bs = beatmap['beatmapset']

    title  = bs.get('title_unicode')  or bs['title']
    artist = bs.get('artist_unicode') or bs['artist']

    if beatmap:
        await channel.send(
            f"🎯 【osu!】今日のデイリーチャレンジ\n\n"
            f"{artist} - {title}\n"
            f"難易度: {beatmap["difficulty_rating"]}\n"
            f"https://osu.ppy.sh/beatmapsets/{beatmap['beatmapset']['id']}#{beatmap['mode']}/{beatmap['id']}"
        )
    """

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("c!daily"):
        channel = message.channel
        token = await osu.get_osu_token()
        beatmap = await osu.get_daily_beatmap(token)

        if beatmap:
            bs = beatmap['beatmapset']
            title  = bs.get('title_unicode')  or bs['title']
            artist = bs.get('artist_unicode') or bs['artist']

            await channel.send(
                f"🎯 【osu!】今日のデイリーチャレンジ\n\n"
                f"{artist} - {title}\n"
                f"難易度: {beatmap['difficulty_rating']}\n"
                f"https://osu.ppy.sh/beatmapsets/{beatmap['beatmapset']['id']}#{beatmap['mode']}/{beatmap['id']}"
            )
        else:
            await channel.send("今日のデイリーチャレンジは見つかりませんでした。")

client.run(TOKEN)
