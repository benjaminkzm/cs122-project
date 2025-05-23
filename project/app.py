from flask import Flask, render_template, request, jsonify, make_response
from steamapi import fetch_game_data, fetch_overall_reviews, fetch_all
from google.cloud import firestore
from datetime import datetime, timedelta
import csv
from io import StringIO

app = Flask(__name__)

# Firestore client initialization
try:
    db = firestore.Client()
except:
    db = None

GAME_APPIDS = fetch_all()

# Build a lowercase name→appid lookup
NAME_TO_APPID = {name.lower(): appid for appid, name in GAME_APPIDS.items()}

@app.route('/')
def index():
    return render_template('index.html', game_data=None)

@app.route('/search')
def search():
    query = (request.args.get('query') or "").strip()
    if not query:
        return "No query provided.", 400

    # Decide if query is an AppID or a game name
    if query.isdigit():
        appid = int(query)
    else:
        appid = NAME_TO_APPID.get(query.lower())
        if appid is None:
            return f"Unknown game name '{query}'.", 404

    # Fetch core Steam info
    game_data = fetch_game_data(appid)
    if not game_data:
        return f"No data for AppID {appid}.", 404

    # Fetch review breakdown
    stats = fetch_overall_reviews(appid) or {}
    game_data['review_positive'] = stats.get('positive_pct')
    game_data['review_negative'] = stats.get('negative_pct')
    game_data['review_total']    = stats.get('total')

    return render_template('index.html', game_data=game_data)

@app.route('/history/<int:appid>')
def history_game(appid):
    if db is None:
        return "History unavailable (no Firestore)", 500
    name = GAME_APPIDS.get(appid)
    if not name:
        return "Unknown AppID", 404

    # Default to the past 24 hours
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

    # Query only on timestamp—avoid needing a composite index
    docs = (
        db.collection('player_counts')
          .where('timestamp', '>=', start_dt)
          .where('timestamp', '<',  end_dt)
          .order_by('timestamp')
          .stream()
    )

    data = []
    for doc in docs:
        rec = doc.to_dict()
        if rec.get('appid') != appid:
            continue
        data.append({
            'timestamp': rec['timestamp'].isoformat(),
            'count':     rec['player_count']
        })

    return jsonify(data)

@app.route('/export/history/<int:appid>')
def export_history(appid):
    start_str = request.args.get('start')
    end_str   = request.args.get('end')
    try:
        start_dt = datetime.fromisoformat(start_str)
        end_dt   = datetime.fromisoformat(end_str) + timedelta(days=1)
    except Exception:
        return "Invalid date format", 400

    docs = (
        db.collection('player_counts')
          .where('timestamp', '>=', start_dt)
          .where('timestamp', '<',  end_dt)
          .order_by('timestamp')
          .stream()
    )

    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(['timestamp','player_count'])
    for doc in docs:
        d = doc.to_dict()
        if d.get('appid') != appid:
            continue
        writer.writerow([d['timestamp'].isoformat(), d['player_count']])

    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'text/csv'
    resp.headers['Content-Disposition'] = (
        f'attachment; filename=history_{appid}_{start_str}_to_{end_str}.csv'
    )
    return resp

if __name__ == '__main__':
    app.run(debug=True)
