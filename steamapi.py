import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs


def fetch_game_data(appid):
    """Fetch player count + store info (incl. header_image) for a given AppID."""
    try:
        # 1) Player count
        pr = requests.get(
            f"https://api.steampowered.com/ISteamUserStats/"
            f"GetNumberOfCurrentPlayers/v1/?appid={appid}",
            timeout=5
        ).json().get("response", {})
        player_count = pr.get("player_count", 0)

        # 2) Store details — ask for US / English
        store_url = (
            "https://store.steampowered.com/api/appdetails"
            f"?appids={appid}&cc=US&l=en"
        )
        jr = requests.get(store_url, timeout=5).json().get(str(appid), {})

        # If Steam says `success: false`, there's no data (no image, no name, etc)
        if not jr.get("success", False):
            print(f"❌ Store API returned success=false for {appid}")
            return None

        data = jr["data"]

        # Now you can safely grab the header image, screenshots, etc:
        header_image = data.get("header_image")  # this will now exist
        screenshots  = [s["path_full"] for s in data.get("screenshots", [])]
        videos       = [m["webm"]["max"] for m in data.get("movies",[])
                        if m.get("webm")]

        # 3) Price + name
        price = 0.0
        if data.get("price_overview"):
            price = data["price_overview"]["final"] / 100.0

        name = data.get("name", "Unknown Game")

        # 4) Descriptions (clean HTML)
        def clean(raw):
            return bs(raw or "", "html.parser").get_text(" ", strip=True)

        short_desc     = clean(data.get("short_description"))
        detailed_desc  = clean(data.get("detailed_description"))
        
        # 5) Developer / publisher
        devs = data.get('developers', [])
        developer = ", ".join(devs) if devs else "Unknown"
        
        # 6) Publisher
        pubs = data.get("publishers", [])
        publisher = ", ".join(pubs) if pubs else "Unknown"

        # 7) Release date
        rd = data.get("release_date", {})
        release_date = rd.get("date", "Unknown")

        return {
            "appid": appid,
            "name": name,
            "player_count": player_count,
            "price": price,
            "short_description": short_desc,
            "detailed_description": detailed_desc,
            "header_image": header_image,
            "screenshots": screenshots,
            "video_urls": videos,
            'developer': developer,
            "publisher": publisher,
            "release_date": release_date
        }

    except Exception as e:
        print(f"⚠️ Error fetching data for {appid}: {e}")
        return None


def clean(raw_desc):
    """Clean the raw description by removing HTML tags."""
    soup = bs(raw_desc, 'html.parser')
    return soup.get_text(separator=' ', strip=True)
 
def fetch_all():
    """Fetch all games on the Steam database and return AppIDs and names."""
    all_games_data = {}
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        app_list = data['applist']['apps']
        
        # Convert the list of dictionaries into a dictionary of AppID -> Game Name
        for app in app_list:
            appid = app['appid']
            name = app['name']
            all_games_data[appid] = name  # Map AppID to Game Name
        
        return all_games_data
    else:
        raise Exception("Failed to fetch Steam Apps")
    
def fetch_overall_reviews(appid):
    """Fetch overall reviews from SteamSpy API."""
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None

    data = resp.json()
    positives = data.get('positive', 0)
    negatives = data.get('negative', 0)
    total     = positives + negatives

    if total == 0:
        return {
            "positive_pct": None,
            "negative_pct": None,
            "total": 0
        }

    pos_pct = round((positives / total) * 100, 1)
    neg_pct = round((negatives / total) * 100, 1)

    return {
        "positive_pct": pos_pct,
        "negative_pct": neg_pct,
        "total": total
    }