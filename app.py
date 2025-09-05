# app.py
import streamlit as st
import pandas as pd
from analyze import classify_sentiment, classify_urgency, extract_info, draft_reply
from priority import compute_priority
from datetime import datetime
import re

st.set_page_config(page_title="📧 AI-Powered Email Assistant", layout="wide")

# --- Helpers ---


def extract_name_from_email(email):
    """
    Extracts the first part of the email (before @) and formats it as a name.
    alice@xyz.com -> Alice
    john.doe@abc.com -> John
    """
    name_part = email.split("@")[0]
    name = re.split(r"[._]", name_part)[0]  # john.doe -> john
    return name.capitalize()


@st.cache_data
def process_emails(df):
    results = []
    for i, row in df.iterrows():
        text = f"{row['subject']} {row['body']}"
        sentiment = classify_sentiment(text)['sentiment']
        urgency = classify_urgency(text)
        extracted = extract_info(text)

        # Extract name from sender email
        name = extract_name_from_email(row['sender'])
        reply = draft_reply(name, text, sentiment, urgency, extracted)

        # Personalize reply
        if isinstance(reply, str):
            if "{name}" in reply:
                reply = reply.replace("{name}", name)
            else:
                reply = f"Hi {name},\n\n" + reply

        priority = compute_priority(sentiment, urgency, row['sent_date'])

        results.append({
            "sender": row['sender'],
            "name": name,
            "subject": row['subject'],
            "sentiment": sentiment,
            "urgency": urgency,
            "priority": priority,
            "reply": reply,
            "extracted": extracted,
            "body": row['body'],
            "sent_date": row['sent_date']
        })

    return pd.DataFrame(results).sort_values("priority", ascending=False)


# --- File uploader ---
uploaded_file = st.file_uploader(
    "📂 Upload a CSV file with email data", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, parse_dates=["sent_date"])
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        st.stop()

    # Process emails (cached)
    res_df = process_emails(df)

    # Sidebar filters
    st.sidebar.header("Filters")
    urg_filter = st.sidebar.selectbox(
        "Urgency", ["All", "urgent", "not urgent"])
    sent_filter = st.sidebar.selectbox(
        "Sentiment", ["All", "positive", "neutral", "negative"]
    )

    filtered_df = res_df.copy()
    if urg_filter != "All":
        filtered_df = filtered_df[filtered_df['urgency'] == urg_filter]
    if sent_filter != "All":
        filtered_df = filtered_df[filtered_df['sentiment'] == sent_filter]

    # Dashboard
    st.title("📧 AI-Powered Email Assistant")
    st.subheader("Support Emails")

    for idx, row in filtered_df.iterrows():
        with st.expander(
            f"{row['sender']} | {row['subject']} | {row['urgency'].upper()} | {row['sentiment']}"
        ):
            st.write(f"**Date:** {row['sent_date']}")
            st.write(f"**Body:** {row['body']}")
            st.json(row['extracted'])
            st.text_area("AI Draft Reply", value=row['reply'], height=200)
            st.button("✅ Approve & Send", key=f"approve_{idx}")

else:
    st.info("👆 Please upload a CSV file to start processing.")
