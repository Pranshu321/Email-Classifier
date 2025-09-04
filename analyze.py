
import os
import json
from groq import Groq
import dotenv

dotenv.load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def classify_sentiment(text):
    prompt = f"""
    Classify the sentiment of this email as Positive, Neutral, or Negative.
    Email: {text}
    Respond in JSON with key 'sentiment'.
    """
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(resp.choices[0].message.content) # type: ignore


def classify_urgency(text):
    prompt = f"""
    Decide if this email is Urgent or Not Urgent.
    Email: {text}
    Respond ONLY with one of: "urgent", "not urgent".
    """
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    urgency = resp.choices[0].message.content.strip().lower() # type: ignore
    return urgency  # always a string



def extract_info(text):
    prompt = f"""
    Extract details from this email. Return JSON with:
    - phones: []
    - alt_emails: []
    - product: string or null
    - order_id: string or null
    - requirements: [list]
    Email: {text}
    """
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(resp.choices[0].message.content) # type: ignore


def draft_reply(name, email, sentiment, urgency, extracted):
    prompt = f"""
    Write a professional support reply. 
    - Name of recipient is {name}.
    - Be empathetic if sentiment={sentiment}.
    - Address urgency={urgency}.
    - Mention product/order if available: {extracted}.
    Email: {email}
    """
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
