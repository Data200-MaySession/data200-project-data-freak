import streamlit as st
import pandas as pd
import pickle

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

