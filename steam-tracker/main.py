# main.py
import datetime
import requests
from google.cloud import firestore

APP_IDS = [2767030, 570, 730]

def steamTracker(request):
    db = firestore.Client()
    col = db.collection("player_counts")

    for appid in APP_IDS:
        url = (
            "https://api.steampowered.com/"
            "ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
            f"?appid={appid}"
        )
        resp = requests.get(url).json().get("response", {})
        count = resp.get("player_count", 0)
        col.add({
            "appid": appid,
            "timestamp": datetime.datetime.utcnow(),
            "player_count": count
        })

    return "OK", 200
