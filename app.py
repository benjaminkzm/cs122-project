from flask import Flask, render_template, request
import pandas as pd
from steamapi import fetch_game_data
import requests

app = Flask(__name__)

@app.route('/search')
def index():
    query = request.args.get('query')
    if not query:
        return "No query provided.", 400
    
    try:
        appid = int(query)
        # Check if the AppID is valid
        if appid <= 0:
            return "Invalid AppID. Please enter a positive integer.", 400
        game_data = fetch_game_data(appid)
        if game_data is None:
            return "No data found for the provided AppID.", 404
    except ValueError:
        return "Invalid AppID format. Please enter a valid number.", 400
    
    return render_template('index.html', game_data=game_data)

