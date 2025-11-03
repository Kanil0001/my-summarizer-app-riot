# 🔥 LoL Stats Summary Generator

A fast, user-friendly Streamlit web app that pulls League of Legends player stats via the Riot API. Enter a summoner name and region to get instant summaries: ranked tiers, win rates, recent match breakdowns (KDA, CS, gold), pie charts, trends, and CSV exports. Built for summoners who want quick insights without hassle!

![LoL Stats Demo](https://via.placeholder.com/800x400/ff4655/ffffff?text=LoL+Stats+Generator) <!-- Replace with a screenshot of your app -->

## ✨ Features
- **Ranked Overview**: Solo/Duo tier, LP, lifetime win rate.
- **Recent Matches**: Analyze 5-20 games with KDA, CS/min, top champs.
- **Visuals**: Interactive pie charts for wins/losses and bar graphs for KDA trends.
- **Export**: Download detailed stats as CSV.
- **Rate-Limited & Cached**: Respects Riot API limits with smart caching.
- **Mobile-Friendly**: Runs in any browser.

## 🚀 Quick Start (Local)
1. Clone the repo: `git clone https://github.com/yourusername/lol-stats-generator.git`
2. Install deps: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Open [localhost:8501](http://localhost:8501) – add your Riot API key in the sidebar.

**Need a Riot API Key?** Free from [Riot Developer Portal](https://developer.riotgames.com/) (regenerate daily).

## 🌐 Deploy for Free (Automatic Hosting)
- **Streamlit Cloud**: Connect your GitHub repo [here](https://share.streamlit.io/). Auto-deploys on pushes—share a live link!
- **Heroku/Render**: Use their Python templates for always-on access.
- Pro Tip: Set API key as a secret/env var for security.

## 📊 Example Output
For summoner "Doublelift" (NA):
- **Rank**: Challenger I (500 LP)
- **Win Rate**: 58.2% (120W 87L)
- **Recent Avg KDA**: 4.2
- **Top Champ**: Jhin (3 games)

| Match | Outcome | KDA | Champion | CS | Gold |
|-------|---------|-----|----------|----|------|
| 1     | Win    | 8/2/7 | Jhin    | 180| 14k |
| 2     | Loss   | 3/5/4 | Ezreal  | 150| 11k |

## 🔧 Customization
- Add champion mastery: Extend with `/lol/champion-mastery/v4/...` endpoint.
- Scheduled Runs: Use cron/PythonAnywhere for daily emails of your stats.
- Themes: Tweak CSS in `app.py` for more LoL flair (e.g., summoner icons).

## ⚠️ Limitations & TOS
- Riot API: 20 reqs/sec, 100/2min—app handles this.
- Data is public; respect [Riot's TOS](https://www.riotgames.com/en/terms-of-service).
- Not affiliated with Riot Games.

## 🤝 Contributing
Fork, PR, or star! Issues? Open one.

**Made with ❤️ for the Rift. GLHF!**  
[Your Name] | [November 2025]

---

[![Streamlit](https://img.shields.io/badge/Powered%20by-Streamlit-ff4655?logo=streamlit)](https://streamlit.io) [![Riot API](https://img.shields.io/badge/API-Riot%20Games-00a8ff)](https://developer.riotgames.com/)