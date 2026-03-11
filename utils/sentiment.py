from textblob import TextBlob
import pandas as pd

POSITIVE_WORDS = [
    "bello", "bellissimo", "fantastico", "ottimo", "stupendo", "meraviglioso",
    "adoro", "amo", "perfetto", "eccellente", "incredibile", "emozionante",
    "divertente", "spettacolare", "bomba", "epico", "top", "bravo", "bravissimi"
]

NEGATIVE_WORDS = [
    "pessimo", "brutto", "orribile", "schifo", "deludente", "noia", "noioso",
    "insopportabile", "odio", "terribile", "inutile", "peggio", "finito",
    "ingiusto", "sopravvalutato", "teatrale"
]

def analyze_sentiment_italian(text):
    text_lower = str(text).lower()
    pos_count = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg_count = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    italian_score = (pos_count - neg_count) * 0.3
    try:
        blob = TextBlob(text)
        blob_score = blob.sentiment.polarity * 0.7
    except:
        blob_score = 0
    final_score = italian_score + blob_score
    if final_score > 0.05:
        label = "positivo"
        emoji = "😊"
    elif final_score < -0.05:
        label = "negativo"
        emoji = "😠"
    else:
        label = "neutro"
        emoji = "😐"
    return label, round(final_score, 3), emoji

def analyze_dataframe(df):
    df = df.copy().reset_index(drop=True)
    labels = []
    scores = []
    emojis = []
    for text in df["text"]:
        label, score, emoji = analyze_sentiment_italian(text)
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
        "il", "la", "lo", "le", "gli", "i", "un", "una", "uno",
        "di", "da", "in", "su", "per", "con", "tra", "fra",
        "e", "o", "ma", "che", "è", "si", "non", "mi", "ti",
        "ci", "vi", "li", "le", "ne", "a", "ai", "al", "agli",
        "del", "della", "dei", "delle", "degli", "questo", "questa",
        "questi", "queste", "ho", "ha", "hanno", "sono", "era",
        "stasera", "sempre", "anche", "più", "tutto", "tutti"
    }
    all_words = []
    for text in df["text"]:
        words = str(text).lower().split()
        for word in words:
            word = word.strip(".,!?#@\"'()")
            word = word.replace("#pechinoexpress2026", "").replace("#pechinoexpress", "")
            if len(word) > 3 and word not in stopwords and not word.startswith("http"):
                all_words.append(word)
    from collections import Counter
    return dict(Counter(all_words).most_common(top_n))
