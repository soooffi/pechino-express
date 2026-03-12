import requests
import pandas as pd
from datetime import datetime
import streamlit as st

def get_tweets_by_hashtag(hashtag: str, max_results: int = 100) -> pd.DataFrame:
    """
    Chiama l'API reale di X e restituisce i tweet per l'hashtag dato.
    Usa il Bearer Token salvato in .streamlit/secrets.toml
    """
    # Prende il token dai secrets di Streamlit
    bearer_token = st.secrets["BEARER_TOKEN"]

    # Prepara la query — cerca tweet recenti con l'hashtag
    query = f"{hashtag} lang:it -is:retweet"

    # Endpoint dell'API X v2
    url = "https://api.twitter.com/2/tweets/search/recent"

    # Parametri della richiesta
    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,text",
        "expansions": "author_id",
        "user.fields": "username"
    }

    # Header con autenticazione
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "PechinoExpressSentiment/1.0"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if "data" not in data:
            return pd.DataFrame()

        # Mappa user_id → username
        users = {}
        if "includes" in data and "users" in data["includes"]:
            for user in data["includes"]["users"]:
                users[user["id"]] = user["username"]

        # Costruisce il DataFrame
        rows = []
        for tweet in data["data"]:
            metrics = tweet.get("public_metrics", {})
            rows.append({
                "text": tweet["text"],
                "likes": metrics.get("like_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "timestamp": tweet.get("created_at", datetime.now().isoformat()),
                "username": users.get(tweet.get("author_id", ""), "utente_x"),
                "hashtag": hashtag
            })

        df = pd.DataFrame(rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    except requests.exceptions.HTTPError as e:
        st.error(f"Errore API X: {e.response.status_code} — {e.response.text}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Errore generico: {str(e)}")
        return pd.DataFrame()
