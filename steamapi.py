import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs


def fetch_game_data(appid):
    """Fetch player count and price data from Steam API based on AppID."""
    try:
        # Fetch player count
        player_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
        player_response = requests.get(player_url)
        player_data = player_response.json().get('response', {})
        player_count = player_data.get('player_count', 0)  # Default to 0 if no player count available
        
        # Fetch price and game name
        price_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        price_response = requests.get(price_url)
        
        if price_response.status_code != 200:
            print(f"Failed to fetch price information for appid {appid}")
            return None  # Skip games without price data
        
        # Check if the response contains valid JSON
        price_data_json = price_response.json()
        
        if price_data_json is None or str(appid) not in price_data_json or 'data' not in price_data_json[str(appid)]:
            print(f"No valid price data available for appid {appid}")
            return None  # Skip games without valid price data
        
        # Safely get price data
        price_data = price_data_json[str(appid)].get('data', None)
        
        if not price_data:
            print(f"No price data found for appid {appid}")
            return None  # Skip games without price data

        name = price_data.get('name', 'Unknown Game')
        price = 0.0  # Default price if no valid price information

        if 'price_overview' in price_data and price_data['price_overview'] is not None:
            price_cents = price_data['price_overview'].get('final', 0)
            price = price_cents / 100  # Convert cents to dollars

        # Fetch game description
        short_description = price_data.get('short_description', 'No description available')
        detailed_description = price_data.get('detailed_description', 'No detailed description available')
        short_description = clean(short_description) # clean raw html
        detailed_description = clean(detailed_description) 

        # Fetch video (trailers, etc.) if available
        videos = price_data.get('movies', [])
        video_urls = [video['webm']['max'] for video in videos if 'webm' in video]
        screenshots = [s['path_full'] for s in price_data.get('screenshots', [])]
        
        # Images
        header_image = price_data.get('header_image')

        return {
            'appid': appid,
            'name': name,
            'player_count': player_count,
            'price': price,
            'short_description': short_description,
            'detailed_description': detailed_description,
            'video_urls': video_urls,
            'header_image': header_image,
            'screenshots': screenshots
        }

    except Exception as e:
        print(f"Error fetching data for appid {appid}: {e}")
        return None  # Skip this game if an error occurs


def clean(raw_desc):
    """Clean the raw description by removing HTML tags."""
    soup = bs(raw_desc, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

# Tester
game = fetch_game_data(440)  # Example usage
print(game['name'])  # Print the fetched game data
print(game['player_count'])  # Print the fetched game data
print(game['price'])  # Print the fetched game data
print(game['short_description'])  # Print the fetched game data
print(game['detailed_description'])  # Print the fetched game data
print(game['video_urls'])  # Print the fetched game data
print(game['screenshots'])  # Print the fetched game data