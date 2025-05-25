import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

OSU_CLIENT_ID = os.getenv("OSU_CLIENT_ID")
OSU_CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET")

async def get_osu_token():
    print("Fetching osu! API token...")
    async with aiohttp.ClientSession() as session:
        async with session.post("https://osu.ppy.sh/oauth/token", data={
            "client_id": OSU_CLIENT_ID,
            "client_secret": OSU_CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "public"
        }) as res:
            data = await res.json()
            return data["access_token"]

async def get_daily_beatmap(token):
    print("Fetching daily beatmap...")
    headers = {"Authorization": f"Bearer {token}", "Accept-Language": "ja"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("https://osu.ppy.sh/api/v2/rooms") as res:
            rooms = await res.json()

        for room in rooms:
            if room.get("category") == "daily_challenge":
                current = room.get("current_playlist_item")
                if current and current.get("beatmap_id"):
                    beatmap_id = current["beatmap_id"]
                    async with session.get(
                        f"https://osu.ppy.sh/api/v2/beatmaps/{beatmap_id}"
                    ) as res:
                        return await res.json()
    return None
