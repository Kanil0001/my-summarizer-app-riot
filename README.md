# LoL Stats Summary Generator

**Hackathon Project — Streamlit app**  
Automatically fetches and summarizes a League of Legends player's recent match stats using the Riot API. Includes interactive charts, CSV export, and a demo mode for testing without an API key.

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-ff4655?logo=streamlit)](https://streamlit.io)
[![Riot API](https://img.shields.io/badge/API-Riot%20Games-00a8ff)](https://developer.riotgames.com/)

---

## Features
- Ranked overview: tier, LP, lifetime win rate.  
- Recent matches: KDA, CS, gold, champion breakdown.  
- Visuals: KDA trend, win/loss pie, champion distribution.  
- Export: download match data as CSV.  
- Demo mode: run without a Riot API key for offline/dev demos.  
- Rate-limited & cached to respect Riot API limits.

---

## 🛠 Tech stack
- Python 3
- Streamlit
- Pandas, Matplotlib
- Riot Games API

---

## Quick start (local)
1. Clone the repo:
   ```bash
   git clone https://github.com/kanil0001/my-summarizer-app-riot.git
   cd my-summarizer-app-riot
