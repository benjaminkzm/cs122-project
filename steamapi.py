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

#test
appid = 1113000
game_data = fetch_game_data(appid)
print(game_data)

