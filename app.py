
import streamlit as st
import requests
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import json
import time

# Page config
st.set_page_config(page_title="Game Stats Summary Generator", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5em; color: #ff4655; text-align: center; margin-bottom: 1em;}
    .metric-box {background-color: #1f1f1f; padding: 1em; border-radius: 10px; text-align: center; margin-bottom: 1em;}
    .metric-value {font-size: 2em; color: #ff4655; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">League of Legends Stats Generator</h1>', unsafe_allow_html=True)

# Sidebar config
st.sidebar.header("Configuration")
demo_mode = st.sidebar.checkbox("Use Demo Data (no API key)")
api_key = ""
if not demo_mode:
    api_key = st.sidebar.text_input("Riot API Key", type="password", help="Get from Riot Developer Portal – expires every 24h.")
summoner_name = st.sidebar.text_input("Summoner Name", value="Doublelift")
platform = st.sidebar.selectbox("Region", ["na1", "euw1", "kr", "eun1", "jp1"])
match_count = st.sidebar.slider("Recent Matches", 3, 20, 5)

if not demo_mode and not api_key:
    st.sidebar.warning("Enter Riot API key to fetch live data!")
    st.stop()

BASE_URL = f"https://{platform}.api.riotgames.com"

# ----------- API / Demo Functions -----------

def load_demo_data():
    with open("mock_matches.json") as f:
        return json.load(f)

@st.cache_data(ttl=3600)
def get_summoner_info(name, api_key):
    url = f"{BASE_URL}/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}"
    time.sleep(0.1)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        st.error(f"Summoner '{name}' not found or API issue.")
        return None

@st.cache_data(ttl=3600)
def get_ranked_stats(summoner_id, api_key):
    url = f"{BASE_URL}/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    time.sleep(0.1)
    r = requests.get(url)
    return r.json() if r.status_code == 200 else []

@st.cache_data(ttl=3600)
def get_match_ids(puuid, count, api_key):
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}&api_key={api_key}"
    time.sleep(0.1)
    r = requests.get(url)
    return r.json() if r.status_code == 200 else []

@st.cache_data(ttl=3600)
def get_match_details(match_id, api_key):
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}?api_key={api_key}"
    time.sleep(0.1)
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# ----------- Main Logic -----------

if st.sidebar.button("Generate"):
    with st.spinner("Fetching data..."):
        try:
            # Fetch Summoner
            if demo_mode:
                matches = load_demo_data()
                summoner = {"id": "demo_id", "puuid": "demo_player", "name": "DemoPlayer", "summonerLevel": 100}
                leagues = [{"queueType":"RANKED_SOLO_5x5","tier":"Gold","rank":"II","leaguePoints":50,"wins":12,"losses":8}]
            else:
                summoner = get_summoner_info(summoner_name, api_key)
                if not summoner: st.stop()
                leagues = get_ranked_stats(summoner['id'], api_key)
                match_ids = get_match_ids(summoner['puuid'], match_count, api_key)
                matches = []
                for mid in match_ids:
                    m = get_match_details(mid, api_key)
                    if m:
                        p = next((p for p in m['info']['participants'] if p['puuid']==summoner['puuid']), None)
                        if p:
                            matches.append({
                                "win": p['win'],
                                "kills": p['kills'],
                                "deaths": p['deaths'],
                                "assists": p['assists'],
                                "champion": p['championName'],
                                "cs": p['totalMinionsKilled'],
                                "gold": p['goldEarned']
                            })

            # Display basic metrics
            st.subheader(f"Summoner: {summoner['name']} | Level {summoner['summonerLevel']}")
            solo_duo = next((l for l in leagues if l['queueType']=="RANKED_SOLO_5x5"), None)
            if solo_duo:
                wins = solo_duo['wins']; losses=solo_duo['losses']; total=wins+losses
                win_rate = wins/total*100 if total>0 else 0
                st.metric("Rank", f"{solo_duo['tier']} {solo_duo['rank']} ({solo_duo['leaguePoints']} LP)")
                st.metric("Win Rate", f"{win_rate:.1f}%")
                st.metric("Record", f"{wins}W {losses}L")

            # Match DataFrame
            df = pd.DataFrame(matches)
            if not df.empty:
                avg_kda = mean((r['kills']+r['assists'])/max(r['deaths'],1) for _, r in df.iterrows())
                avg_cs = df['cs'].mean()
                top_champ = df['champion'].mode()[0]
                recent_win_rate = (df['win'].sum()/len(df))*100

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Recent Win Rate", f"{recent_win_rate:.1f}%")
                col2.metric("Avg KDA", f"{avg_kda:.2f}")
                col3.metric("Avg CS", f"{avg_cs:.0f}")
                col4.metric("Top Champ", top_champ)

                # Charts
                with st.expander("Charts"):
                    # Win/Loss Pie
                    fig1, ax1 = plt.subplots()
                    df['win'].value_counts().plot(kind='pie', ax=ax1, autopct='%1.1f%%', colors=['#4CAF50','#F44336'])
                    ax1.set_ylabel("")
                    ax1.set_title("Recent Win/Loss")
                    st.pyplot(fig1)

                    # KDA Trend
                    fig2, ax2 = plt.subplots()
                    kda_values = [(r['kills']+r['assists'])/max(r['deaths'],1) for _, r in df.iterrows()]
                    ax2.plot(range(1,len(kda_values)+1), kda_values, marker='o', color='#FF9800')
                    ax2.set_xlabel("Match # (Recent → Old)")
                    ax2.set_ylabel("KDA")
                    ax2.set_title("KDA Trend")
                    st.pyplot(fig2)

                    # Champion Pie
                    fig3, ax3 = plt.subplots()
                    df['champion'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax3)
                    ax3.set_ylabel("")
                    ax3.set_title("Champion Distribution")
                    st.pyplot(fig3)

                st.subheader("Match Details")
                st.dataframe(df[['win','kills','deaths','assists','champion','cs','gold']], use_container_width=True)

                # CSV Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, f"{summoner['name']}_stats.csv", "text/csv")

        except Exception as e:
            st.error(f"Error: {str(e)}")

            
        except Exception as e:
            st.error(f"Oops! Error: {str(e)}. Check API key, name, or rates.")

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ using Riot API & Streamlit. Regenerate key daily! For issues, check console.*")

