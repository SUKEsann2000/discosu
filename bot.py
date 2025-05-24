import discord
import requests
import asyncio

from dotenv import load_dotenv
load_dotenv()

import os

import json

TOKEN = os.getenv("DISCORD_TOKEN")
OSU_CLIENT_ID = os.getenv("OSU_CLIENT_ID")
OSU_CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def get_osu_token():
    res = requests.post("https://osu.ppy.sh/oauth/token", data={
        "client_id": OSU_CLIENT_ID,
        "client_secret": OSU_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "public"
    }).json()
    return res["access_token"]

async def get_daily_beatmap(token):
    headers = {"Authorization": f"Bearer {token}", "Accept-Language": "ja"}
    res = requests.get("https://osu.ppy.sh/api/v2/rooms", headers=headers).json()

    for room in res:
        if room.get("category") == "daily_challenge":
            current = room.get("current_playlist_item")
            if current and current.get("beatmap_id"):
                beatmap_id = current["beatmap_id"]
                beatmap = requests.get(
                    f"https://osu.ppy.sh/api/v2/beatmaps/{beatmap_id}",
                    headers=headers
                ).json()
                return beatmap
    return None


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
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
    await client.close()

client.run(TOKEN)
