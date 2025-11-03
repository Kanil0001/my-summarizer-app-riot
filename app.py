import streamlit as st
import requests
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import time  # For rate limiting

# Page config
st.set_page_config(page_title="LoL Stats Summary Generator", layout="wide")

# Custom CSS for better look
st.markdown("""
<style>
    .main-header {font-size: 2.5em; color: #ff4655; text-align: center; margin-bottom: 2em;}
    .metric-box {background-color: #1f1f1f; padding: 1em; border-radius: 10px; text-align: center;}
    .metric-value {font-size: 2em; color: #ff4655; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🔥 League of Legends Stats Generator</h1>', unsafe_allow_html=True)
st.write("Enter a summoner's name and region to fetch their ranked stats, recent matches, and more. Powered by Riot API.")

# Sidebar for inputs
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Riot API Key", type="password", help="Get from [Riot Developer Portal](https://developer.riotgames.com/) – expires every 24h.")
summoner_name = st.sidebar.text_input("Summoner Name", value="Doublelift", help="e.g., Faker")
platform = st.sidebar.selectbox("Region", ["na1", "euw1", "kr", "eun1", "jp1"], index=0, help="Server region")
match_count = st.sidebar.slider("Recent Matches to Analyze", 5, 20, 10)

if not api_key:
    st.sidebar.warning("Enter your API key to start!")
    st.stop()

# Base URL
BASE_URL = f"https://{platform}.api.riotgames.com"

@st.cache_data(ttl=3600)  # Cache for 1 hour to respect rates
def get_summoner_info(name, api_key):
    url = f"{BASE_URL}/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}"
    time.sleep(0.1)  # Gentle rate limit
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Summoner '{name}' not found on {platform.upper()}. Try another name or region.")
        return None

@st.cache_data(ttl=3600)
def get_ranked_stats(summoner_id, api_key):
    url = f"{BASE_URL}/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}"
    time.sleep(0.1)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

@st.cache_data(ttl=3600)
def get_match_ids(puuid, count, api_key):
    url = f"{BASE_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}&api_key={api_key}"
    time.sleep(0.1)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

@st.cache_data(ttl=3600)
def get_match_details(match_id, api_key):
    url = f"{BASE_URL}/lol/match/v5/matches/{match_id}?api_key={api_key}"
    time.sleep(0.1)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Main logic
if st.sidebar.button("Generate Stats! 🚀", type="primary"):
    with st.spinner("Fetching data..."):
        try:
            # Step 1: Summoner info
            summoner = get_summoner_info(summoner_name, api_key)
            if not summoner:
                st.stop()
            summoner_id = summoner['id']
            puuid = summoner['puuid']
            level = summoner['summonerLevel']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Level", level)
            with col2:
                st.metric("Summoner", summoner['name'])
            with col3:
                st.metric("Region", platform.upper())
            
            # Step 2: Ranked stats
            leagues = get_ranked_stats(summoner_id, api_key)
            solo_duo = next((l for l in leagues if l['queueType'] == 'RANKED_SOLO_5x5'), None)
            
            if solo_duo:
                wins = int(solo_duo['wins'])
                losses = int(solo_duo['losses'])
                total_games = wins + losses
                win_rate = (wins / total_games * 100) if total_games > 0 else 0
                rank_str = f"{solo_duo['tier']} {solo_duo['rank']} ({solo_duo['leaguePoints']} LP)"
                
                col4, col5, col6 = st.columns(3)
                with col4:
                    st.markdown(f'<div class="metric-box"><div class="metric-value">{rank_str}</div><small>Rank</small></div>', unsafe_allow_html=True)
                with col5:
                    st.markdown(f'<div class="metric-box"><div class="metric-value">{win_rate:.1f}%</div><small>Win Rate</small></div>', unsafe_allow_html=True)
                with col6:
                    st.markdown(f'<div class="metric-box"><div class="metric-value">{wins}W {losses}L</div><small>Record</small></div>', unsafe_allow_html=True)
            else:
                st.warning("No ranked data available (unranked player?).")
            
            # Step 3: Recent matches
            match_ids = get_match_ids(puuid, match_count, api_key)
            if not match_ids:
                st.error("No recent matches found.")
                st.stop()
            
            match_stats = []
            champ_counts = {}
            for match_id in match_ids:
                match = get_match_details(match_id, api_key)
                if match and 'info' in match:
                    participants = match['info']['participants']
                    player = next((p for p in participants if p['puuid'] == puuid), None)
                    if player:
                        match_stats.append({
                            'win': 'Win' if player['win'] else 'Loss',
                            'kills': player['kills'],
                            'deaths': player['deaths'],
                            'assists': player['assists'],
                            'kda': f"{player['kills']}/{player['deaths']}/{player['assists']}",
                            'champion': player['championName'],
                            'cs': player['totalMinionsKilled'],
                            'gold': player['goldEarned']
                        })
                        champ_counts[player['championName']] = champ_counts.get(player['championName'], 0) + 1
            
            if match_stats:
                df = pd.DataFrame(match_stats)
                recent_wins = (df['win'] == 'Win').sum()
                recent_win_rate = (recent_wins / len(df) * 100)
                avg_kills = df['kills'].mean()
                avg_deaths = df['deaths'].mean()
                avg_assists = df['assists'].mean()
                avg_kda = mean((row['kills'] + row['assists']) / max(row['deaths'], 1) for _, row in df.iterrows())
                avg_cs = df['cs'].mean()
                top_champ = max(champ_counts, key=champ_counts.get) if champ_counts else "N/A"
                
                # Summary row
                col7, col8, col9, col10 = st.columns(4)
                with col7:
                    st.markdown(f'<div class="metric-box"><div class="metric-value">{recent_win_rate:.1f}%</div><small>Recent Win Rate</small></div>', unsafe_allow_html=True)
                with col8:
                    st.markdown(f'<div class="metric-box"><div class="metric-value">{avg_kda:.2f}</div><small>Avg KDA</small></div>', unsafe_allow_html=True)
                with col9:
                    st.markdown(f'<div class="metric-box"><div class="metric-value">{avg_cs:.0f}</div><small>Avg CS</small></div>', unsafe_allow_html=True)
                with col10:
                    st.markdown(f'<div class="metric-box"><div class="metric-value">{top_champ}</div><small>Top Champ</small></div>', unsafe_allow_html=True)
                
                # Charts
                col_a, col_b = st.columns(2)
                with col_a:
                    st.subheader("Recent Win/Loss Pie")
                    fig, ax = plt.subplots()
                    df['win'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=['#4CAF50', '#F44336'])
                    ax.set_title(f"{summoner_name}'s Recent Matches")
                    st.pyplot(fig)
                
                with col_b:
                    st.subheader("KDA per Match")
                    fig, ax = plt.subplots()
                    kda_values = [(row['kills'] + row['assists']) / max(row['deaths'], 1) for _, row in df.iterrows()]
                    ax.bar(range(len(df)), kda_values, color='#FF9800')
                    ax.set_xlabel('Match # (Recent to Old)')
                    ax.set_ylabel('KDA')
                    ax.set_title('KDA Trend')
                    st.pyplot(fig)
                
                # Detailed table
                st.subheader("Match Details")
                st.dataframe(df[['win', 'kda', 'champion', 'cs', 'gold']], use_container_width=True)
                
                # Download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, f"{summoner_name}_stats.csv", "text/csv")
            
        except Exception as e:
            st.error(f"Oops! Error: {str(e)}. Check API key, name, or rates.")

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ using Riot API & Streamlit. Regenerate key daily! For issues, check console.*")