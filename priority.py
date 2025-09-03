# priority.py
import datetime


def compute_priority(sentiment, urgency, sent_date):
    score = 0
    if urgency.lower() == "urgent":
        score += 1.0
    if sentiment.lower() == "negative":
        score += 0.5
    # recency boost (last 24h = higher score)
    now = datetime.datetime.utcnow()
    age_hours = (now - sent_date).total_seconds() / 3600
    if age_hours < 24:
        score += 0.3
    return score
