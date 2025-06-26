import streamlit as st
import pandas as pd
import pickle
<<<<<<< Updated upstream

# Load model
with open("run_predictor_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🏏 IPL Run Predictor")
st.markdown("Predict runs scored (if batting first) or runs conceded (if bowling first) based on match conditions.")

st.sidebar.header("Match Conditions")

teams = [
    "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Rajasthan Royals", "Delhi Capitals",
    "Sunrisers Hyderabad", "Kings XI Punjab", "Lucknow Super Giants", "Gujarat Titans"
]

venues = [
    "Wankhede Stadium", "M Chinnaswamy Stadium", "Eden Gardens",
    "Arun Jaitley Stadium", "Narendra Modi Stadium", "MA Chidambaram Stadium",
    "Punjab Cricket Association Stadium, Mohali"
]

# Sidebar inputs
team = st.sidebar.selectbox("Your Team", teams)
opponent = st.sidebar.selectbox("Opponent Team", [t for t in teams if t != team])
venue = st.sidebar.selectbox("Venue", venues)
match_type = st.sidebar.selectbox("Match Type", ["League", "Playoff", "Final"])
toss_decision = st.sidebar.selectbox("Toss Decision", ["bat", "field"])
role = st.sidebar.radio("Are you batting or bowling first?", ["batting", "bowling"])

# Create input DataFrame with required columns
input_df = pd.DataFrame({
    "our_team": [team],
    "opponent_team": [opponent],
    "venue": [venue],
    "toss_decision": [toss_decision],
    "match_type": [match_type],
    "role": [role]
})

# Predict
if st.sidebar.button("Predict"):
    try:
        prediction = model.predict(input_df)[0]
        st.subheader("📊 Prediction")

        if role == "batting":
            st.success(f"Estimated runs **scored**: {int(prediction)}")
        else:
            st.warning(f"Estimated runs **conceded**: {int(prediction)}")
    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")

=======
import matplotlib.pyplot as plt

# Load model and stats
with open("score_predictor_model.pkl", "rb") as f:
    model = pickle.load(f)

best_batsman = pd.read_csv("stats_best_batsman.csv")
best_bowler = pd.read_csv("stats_best_bowler.csv")
matches = pd.read_csv("matches.csv")

st.set_page_config(layout="wide")
st.title("🏏 IPL Score Predictor & Dashboard")

tab1, tab2 = st.tabs(["📊 Dashboard", "🔮 Predict Score"])

# ---------- Tab 2: Score Prediction ----------
with tab2:
    st.header("🔮 Predict First Innings Score (Runs, 4s & 6s)")

    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select Team A", sorted(matches['team1'].dropna().unique()), key="team1")
        team2 = st.selectbox("Select Team B", sorted(matches['team2'].dropna().unique()), key="team2")

    with col2:
        toss_winner = st.selectbox("Toss Winner", [team1, team2], key="toss_winner")
        toss_decision = st.selectbox("Toss Decision", ["bat", "field"], key="toss_decision")

    venue = st.selectbox("Venue", sorted(matches["venue"].dropna().unique()), key="venue")

    # Determine batting and bowling teams
    if toss_decision == "bat":
        batting_team = toss_winner
        bowling_team = team2 if toss_winner == team1 else team1
        role = "bat"
    else:
        bowling_team = toss_winner
        batting_team = team2 if toss_winner == team1 else team1
        role = "bowl"

    if st.button("Predict"):
        input_df = pd.DataFrame([{
            "venue": venue,
            "our_team": batting_team,
            "opponent_team": bowling_team,
            "role": role
        }])
        prediction = model.predict(input_df)[0]
        st.subheader(f"Predicted Score for {batting_team} 🏏")
        st.write(f"Estimated Total Runs: **{round(prediction)}**")
        st.write("Note: This prediction assumes typical match conditions for a first innings.")

# ---------- Tab 1: Dashboard ----------
with tab1:
    st.header("📊 IPL Dashboard: Team & Match Insights")

    col1, col2, col3 = st.columns(3)
    with col1:
        venue_stats = matches.groupby("venue")["target_runs"].mean().sort_values(ascending=False).head(10)
        st.subheader("🏟️ Avg Runs at Top Venues")
        st.bar_chart(venue_stats)

    with col2:
        team_wins = matches["winner"].value_counts().head(10)
        st.subheader("🏆 Most Wins by Teams")
        st.bar_chart(team_wins)

    with col3:
        toss_wins = matches["toss_winner"].value_counts().head(10)
        st.subheader("🎲 Most Toss Wins")
        st.bar_chart(toss_wins)

    st.subheader("🧢 Toss Decisions")
    toss_decision_count = matches["toss_decision"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(toss_decision_count, labels=toss_decision_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("🔥 Top 10 Batsmen")
        st.dataframe(best_batsman)

    with col5:
        st.subheader("💥 Top 10 Bowlers")
        st.dataframe(best_bowler)
>>>>>>> Stashed changes
