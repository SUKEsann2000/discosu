import requests

from dotenv import load_dotenv
load_dotenv()

import os

import json

OSU_CLIENT_ID = os.getenv("OSU_CLIENT_ID")
OSU_CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET")

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

