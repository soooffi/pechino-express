import anthropic
import pandas as pd
import streamlit as st
from collections import Counter

def analyze_sentiment_with_claude(text: str) -> tuple:
    """Usa Claude AI per analizzare il sentiment di un testo italiano."""
    try:
        api_key = st.secrets["ANTHROPIC_API_KEY"]
        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=20,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analizza il sentiment di questo commento su Pechino Express.
Rispondi SOLO con una di queste parole: positivo, negativo, neutro

Commento: {text}"""
                }
            ]
        )

        label = message.content[0].text.strip().lower()
        if label not in ["positivo", "negativo", "neutro"]:
            label = "neutro"

        score = {"positivo": 0.8, "negativo": -0.8, "neutro": 0.0}.get(label, 0.0)
        emoji = {"positivo": "😊", "negativo": "😠", "neutro": "😐"}.get(label, "😐")

        return label, score, emoji

    except Exception as e:
        # Fallback con parole chiave se l'AI non risponde
        return _fallback_sentiment(text)

def _fallback_sentiment(text: str) -> tuple:
    """Analisi di riserva con parole chiave se Claude non è disponibile."""
    POSITIVE_WORDS = ["bello", "bellissimo", "fantastico", "ottimo", "adoro", "perfetto",
                      "incredibile", "emozionante", "spettacolare", "bomba", "epico", "bravo"]
    NEGATIVE_WORDS = ["pessimo", "brutto", "orribile", "schifo", "deludente", "noia",
                      "insopportabile", "odio", "terribile", "inutile", "peggio"]

    text_lower = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    score = (pos - neg) * 0.3

    if score > 0.05:
        return "positivo", score, "😊"
    elif score < -0.05:
        return "negativo", score, "😠"
    return "neutro", 0.0, "😐"

def analyze_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Aggiunge colonne di sentiment a un DataFrame di tweet."""
    df = df.copy().reset_index(drop=True)
    labels, scores, emojis = [], [], []

    for text in df["text"]:
        label, score, emoji = analyze_sentiment_with_claude(text)
        labels.append(label)
        scores.append(score)
        emojis.append(emoji)

    df["sentiment"] = labels
    df["score"] = scores
    df["emoji"] = emojis
    return df

def get_top_tweets(df, sentiment=None, n=5):
    if sentiment is not None:
        filtered = df[df["sentiment"] == sentiment].copy()
    else:
        filtered = df.copy()
    return filtered.nlargest(n, "likes")[["username", "text", "likes", "retweets", "sentiment", "emoji"]]

def get_sentiment_over_time(df):
    df = df.copy()
    df["time_bucket"] = pd.to_datetime(df["timestamp"]).dt.floor("15min").dt.strftime("%H:%M")
    result = {}
    for bucket in sorted(df["time_bucket"].unique()):
        subset = df[df["time_bucket"] == bucket]
        sentiments = list(subset["sentiment"])
        result[bucket] = {
            "positivo": sentiments.count("positivo"),
            "negativo": sentiments.count("negativo"),
            "neutro": sentiments.count("neutro"),
        }
    rows = [{"time_bucket": k, **v} for k, v in result.items()]
    return pd.DataFrame(rows)

def get_word_frequency(df, top_n=30):
    stopwords = {
        "il", "la", "lo", "le", "gli", "i", "un", "una", "uno", "di", "da", "in",
        "su", "per", "con", "tra", "fra", "e", "o", "ma", "che", "è", "si", "non",
        "mi", "ti", "ci", "vi", "ne", "a", "ai", "al", "del", "della", "dei",
        "questo", "questi", "ho", "ha", "hanno", "sono", "era", "stasera",
        "sempre", "anche", "più", "tutto", "tutti"
    }
    all_words = []
    for text in df["text"]:
        for word in str(text).lower().split():
            word = word.strip(".,!?#@\"'()")
            word = word.replace("#pechinoexpress2026", "").replace("#pechinoexpress", "")
            if len(word) > 3 and word not in stopwords and not word.startswith("http"):
                all_words.append(word)
    return dict(Counter(all_words).most_common(top_n))