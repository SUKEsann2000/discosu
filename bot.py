import discord
import requests
import asyncio

from dotenv import load_dotenv
load_dotenv()

import os

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
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get("https://osu.ppy.sh/api/v2/rooms", headers=headers).json()
    for room in res:
        if room["category"] == "daily_challenge":
            playlist = room["playlist"]
            if playlist:
                beatmap_id = playlist[0]["beatmap_id"]
                beatmap = requests.get(
                    f"https://osu.ppy.sh/api/v2/beatmaps/{beatmap_id}",
                    headers=headers
                ).json()
                return beatmap
    return None

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel()
    token = await get_osu_token()
    beatmap = await get_daily_beatmap(token)

    if beatmap:
        await channel.send(
            f"🎯 今日のデイリーチャレンジ\n"
            f"{beatmap['beatmapset']['title']} - {beatmap['version']}\n"
            f"https://osu.ppy.sh/beatmapsets/{beatmap['beatmapset']['id']}#{beatmap['mode']}/{beatmap['id']}"
        )
    await client.close()

client.run(TOKEN)
