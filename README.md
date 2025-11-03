# LoL Stats Summary Generator

**Hackathon Project** – Automatically fetches and summarizes a League of Legends player's latest match stats using Riot API. Includes interactive charts and CSV export.

## Features
- Fetch ranked stats and recent matches
- Displays metrics: Level, Rank, Win Rate, Avg KDA, Avg CS, Top Champion
- Charts: KDA trend, Win/Loss pie, Champion distribution
- Export match data to CSV
- Demo mode (no API key required)

## Tech Stack
- Python 3 + Streamlit
- Riot API
- Matplotlib, Pandas

## How to Run
1. Clone repo:git clone <repo-url>
cd LoL-Stats-Reddit-Hackathon
2. Install dependencies:
pip install -r requirements.txt
3. Run app:
streamlit run app.py
**Note:** For live Riot API data, enter a valid Riot API key (expires every 24h). Otherwise, enable demo mode.

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-ff4655?logo=streamlit)](https://streamlit.io) [![Riot API](https://img.shields.io/badge/API-Riot%20Games-00a8ff)](https://developer.riotgames.com/)