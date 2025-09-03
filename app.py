# app.py
import streamlit as st
import pandas as pd
from analyze import classify_sentiment, classify_urgency, extract_info, draft_reply
from priority import compute_priority
from datetime import datetime

# Load dataset
df = pd.read_csv("data.csv", parse_dates=["sent_date"])

st.title("📧 AI-Powered Email Assistant")

results = []
for i, row in df.iterrows():
    text = f"{row['subject']} {row['body']}"
    sentiment = classify_sentiment(text)['sentiment']
    urgency = classify_urgency(text)
    extracted = extract_info(text)
    reply = draft_reply(text, sentiment, urgency, extracted)
    priority = compute_priority(sentiment, urgency, row['sent_date'])
    results.append({
        "sender": row['sender'],
        "subject": row['subject'],
        "sentiment": sentiment,
        "urgency": urgency,
        "priority": priority,
        "reply": reply,
        "extracted": extracted,
        "body": row['body'],
        "sent_date": row['sent_date']
    })

res_df = pd.DataFrame(results).sort_values("priority", ascending=False)

# Dashboard
st.sidebar.header("Filters")
urg_filter = st.sidebar.selectbox("Urgency", ["All", "urgent", "not urgent"])
sent_filter = st.sidebar.selectbox(
    "Sentiment", ["All", "positive", "neutral", "negative"])

filtered_df = res_df.copy()
if urg_filter != "All":
    filtered_df = filtered_df[filtered_df['urgency'] == urg_filter]
if sent_filter != "All":
    filtered_df = filtered_df[filtered_df['sentiment'] == sent_filter]

st.subheader("Support Emails")
for _, row in filtered_df.iterrows():
    with st.expander(f"{row['sender']} | {row['subject']} | {row['urgency'].upper()} | {row['sentiment']}"):
        st.write(f"**Date:** {row['sent_date']}")
        st.write(f"**Body:** {row['body']}")
        st.json(row['extracted'])
        st.text_area("AI Draft Reply", value=row['reply'], height=200)
        st.button("✅ Approve & Send", key=row['sender'] + row['subject'])
