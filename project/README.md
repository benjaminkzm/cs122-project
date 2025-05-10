# Steam Database Dashboard

A Flask‐powered web app that lets you look up real‐time Steam player counts, prices, and review statistics for your favorite games—and explore historical trends stored in Firestore.

## Features

- **Live lookups** by Steam AppID or title  
- **Real‐time stats**:  
  - Online player count  
  - Price (in USD)  
  - Positive / negative / total review percentages  
- **Historical charts** of player counts (last hour / day / week), with exportable CSV  
- **Responsive UI** with image/video carousels

## Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/benjaminkzm/cs122-project.git
   cd cs122-project/project
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Setting up Firestore API using Google Cloud**
   - Create a Google Cloud project and Firestore database
   - Download your service account JSON and set: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
   - I then pre-populate player_counts collection with 3 game AppIDs.

4. **Run the app**
   ```bash
   flask run

## Usage
- Search for a game by AppID or name on the home page.

- View live stats and a carousel of screenshots and trailers.

- Click “View Player Count History” to open the interactive chart.

- Choose a quick range (1 h, 24 h, 7 d) or manually pick start/end.

- Export the data you see as CSV for further analysis.

## Future Enhancements

If this project continued in another course, I’d:

- Let visitors save favorite games, see personalized dashboards.
- Let users search from common Steam tags (Action, RPG, Indie, etc.) and discover top titles by live player count.
- Improved web page design with more features and visualization on homepage.
- Price tracker to allow users to estimate when a game would be on sale again based on trends or is currently on sale.

