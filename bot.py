import discord

from dotenv import load_dotenv
load_dotenv()
import os

import osu


TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("c!daily"):
        print("Received c!daily command")
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
