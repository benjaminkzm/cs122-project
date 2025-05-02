from flask import Flask, render_template, request
from steamapi import fetch_game_data, fetch_overall_reviews

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', game_data=None)

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return "No query provided.", 400

    try:
        appid = int(query)
        # Check if the AppID is valid
        if appid <= 0:
            raise ValueError
    except ValueError:
        return "Invalid AppID. Please enter a positive integer.", 400

    game_data = fetch_game_data(appid)
    if not game_data:
        return f"No data found for AppID {appid}.", 404

    review_pct = fetch_overall_reviews(appid)
    game_data['review_pct'] = round(review_pct, 1) if review_pct is not None else None

    return render_template('index.html', game_data=game_data)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
