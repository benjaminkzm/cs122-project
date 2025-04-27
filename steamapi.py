import requests
from datetime import datetime
# api_key = 36889908DBE794629D14DAAB1F64AF45

def fetch_game_data(appid):
    """Fetch player count and price data from Steam API based on AppID."""
    # Fetch player count
    player_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
    player_response = requests.get(player_url)
    if player_response.status_code != 200:
        raise Exception("Failed to fetch player count")
    player_count = player_response.json()['response']['player_count']

    # Fetch price and game name
    price_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    price_response = requests.get(price_url)
    if price_response.status_code != 200:
        raise Exception("Failed to fetch price information")
    
    price_data = price_response.json()[str(appid)]['data']
    name = price_data['name']
    if 'price_overview' in price_data:
        price_cents = price_data['price_overview']['final']
        price = price_cents / 100  # convert cents to dollars
    else:
        price = 0.0  # Free games or missing data

    return {
        'name': name,
        'player_count': player_count,
        'price': price
    }

def fetch_all(appids):
    """Fetch all games on the steam database and return APIDS and name."""
    all_games_data = {}
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        app_list = data['applist']['apps']
        return app_list
    else:
        raise Exception("Failed to fetch Steam Apps")

#test
appid = 1113000
game_data = fetch_game_data(appid)
print(game_data)
count = 0
all_games = fetch_all(appid)
for app in all_games:
    print(f"App ID: {app['appid']}, Name: {app['name'].encode('utf-8', 'ignore').decode('utf-8')}") # includes special characters
    count += 1
    
print(f"Total number of games: {count}")
    
