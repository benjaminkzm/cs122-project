# Steam Data Insights

Authors: Benjamin Khor and Sharon Le

# Project Description

This project leverages the Steam API to analyze key aspects of gaming trends. It tracks player count trends for popular games, monitors price fluctuations to alert users about discounts. This platform will present interactive visualizations and real-time data analysis to help gamers make informed decisions.

# Project Outline/Plan

Game Popularity and Trends – Fetch and visualize player count trends over time for top games.

Price Tracker and Deal Finder – Monitor game prices, track historical trends, and alert users when discounts are available.

# Interface Plan

Web-based dashboard (Flask or Streamlit) or Desktop GUI (PyQt or Tkinter) with interactive visualizations.

Users can select a game to view real-time and historical data.

Charts and tables will display trends for player counts, price changes, and matchmaking stats.

# Data Collection and Storage Plan

Use Steam API to fetch real-time player counts, game pricing data, and matchmaking statistics.

Store data in an SQLite or MongoDB database for historical tracking.

Implement caching mechanisms to reduce API request limits.

# Data Analysis and Visualization Plan (Author #2)

Collected data will be processed and analyzed in categories such as pricing trend, popularity and multiplayer activity.

Pricing can be analyzed through price changes over time, this can tell us an estimate of when we can expect the next sale to take place using line chart and heatmaps.

Player count can be analyzed through player active tracking through out the day to see peak hours and interest for the game using line chart.

Multiplayer activity can be estimated using player count as it provides insights to what time is most populated and when it is low, allowing users estimate their wait time in queue.



