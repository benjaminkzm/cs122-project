from flask import Flask, render_template, request, jsonify
from steamapi import fetch_game_data, fetch_overall_reviews
from google.cloud import firestore
from datetime import datetime, timedelta

app = Flask(__name__)

# Firestore client initialization
try:
    db = firestore.Client()
except:
    db = None

# Game AppIDs and names
GAME_APPIDS = {
    2767030: "Marvel Rivals",
    570:     "Dota 2",
    730:     "Counter-Strike 2"
}

# Build a name→appid lookup for text searches
NAME_TO_APPID = {name.lower(): appid for appid, name in GAME_APPIDS.items()}


@app.route('/')
def index():
    # Renders your search page
    return render_template('index.html', game_data=None)


@app.route('/search')
def search():
    query = (request.args.get('query') or "").strip()
    if not query:
        return "No query provided.", 400

    # Determine if query is numeric AppID or a game name
    if query.isdigit():
        appid = int(query)
    else:
        appid = NAME_TO_APPID.get(query.lower())
        if appid is None:
            return f"Unknown game name '{query}'.", 404

    # Fetch live Steam data
    game_data = fetch_game_data(appid)
    if not game_data:
        return f"No data for AppID {appid}.", 404

    # Fetch reviews percentage
    review_pct = fetch_overall_reviews(appid)
    game_data['review_pct'] = round(review_pct, 1) if review_pct is not None else None

    return render_template('index.html', game_data=game_data)


@app.route('/history/<int:appid>')
def history_game(appid):
    if db is None:
        return "History unavailable (no Firestore)", 500
    name = GAME_APPIDS.get(appid)
    if not name:
        return "Unknown AppID", 404

    # Default last 24h
    now = datetime.utcnow()
    default_start = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
    default_end   = now.strftime("%Y-%m-%dT%H:%M")

    return render_template(
        'history.html',
        appid=appid,
        game_name=name,
        default_start=default_start,
        default_end=default_end
    )


@app.route('/api/history/<int:appid>')
def api_history(appid):
    if db is None:
        return jsonify(error="no db"), 500

    start = request.args.get('start')
    end   = request.args.get('end')
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt   = datetime.fromisoformat(end) + timedelta(days=1)
    except:
        return jsonify(error="invalid date"), 400

    # Query by timestamp, then filter by appid client‐side
    docs = (
        db.collection('player_counts')
          .where('timestamp', '>=', start_dt)
          .where('timestamp', '<',  end_dt)
          .order_by('timestamp')
          .stream()
    )

    data = []
    for d in docs:
        rec = d.to_dict()
        if rec.get('appid') != appid:
            continue
        data.append({
            'timestamp': rec['timestamp'].isoformat(),
            'count':     rec['player_count']
        })
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
