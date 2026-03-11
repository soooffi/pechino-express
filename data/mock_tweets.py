import pandas as pd
import random
from datetime import datetime, timedelta

MOCK_TWEETS = [
    # Positivi
    {"text": "Pechino Express è sempre una bomba! Adoro queste coppie #PechinoExpress", "likes": 342, "sentiment": "positivo"},
    {"text": "Che puntata incredibile stasera!! Mi sono emozionata tantissimo #PechinoExpress2026", "likes": 289, "sentiment": "positivo"},
    {"text": "La coppia formata da quei due è assolutamente la mia preferita ❤️ #PechinoExpress", "likes": 512, "sentiment": "positivo"},
    {"text": "Questo programma è uno dei pochi che guardo ancora in TV. Semplicemente fantastico #PechinoExpress", "likes": 198, "sentiment": "positivo"},
    {"text": "Adoro come si aiutano tra di loro, bellissimo da vedere #PechinoExpress2026", "likes": 421, "sentiment": "positivo"},
    {"text": "Finalmente un reality che mostra il bello del mondo! #PechinoExpress", "likes": 376, "sentiment": "positivo"},
    {"text": "Non riesco a smettere di guardare, troppo bello stasera #PechinoExpress", "likes": 155, "sentiment": "positivo"},
    {"text": "La prova di stasera era epica, bravissimi tutti! #PechinoExpress2026", "likes": 267, "sentiment": "positivo"},
    {"text": "Mi fa venire voglia di viaggiare ogni volta che lo guardo ✈️ #PechinoExpress", "likes": 433, "sentiment": "positivo"},
    {"text": "Che bella coppia, si vede che si vogliono davvero bene #PechinoExpress", "likes": 318, "sentiment": "positivo"},

    # Negativi
    {"text": "Questa puntata è stata una noia mortale, mi aspettavo di più #PechinoExpress", "likes": 87, "sentiment": "negativo"},
    {"text": "Non ce la faccio con questi concorrenti, insopportabili #PechinoExpress2026", "likes": 134, "sentiment": "negativo"},
    {"text": "Il montaggio di stasera era pessimo, si perdeva la continuità #PechinoExpress", "likes": 92, "sentiment": "negativo"},
    {"text": "Eliminati i miei preferiti... programma finito per me #PechinoExpress", "likes": 201, "sentiment": "negativo"},
    {"text": "Ogni anno peggio del precedente. Deludente #PechinoExpress2026", "likes": 76, "sentiment": "negativo"},
    {"text": "Non reggo più questa coppia, troppo teatrale tutto #PechinoExpress", "likes": 143, "sentiment": "negativo"},
    {"text": "La prova era ingiusta, le regole cambiano sempre #PechinoExpress", "likes": 98, "sentiment": "negativo"},
    {"text": "Programma sopravvalutato, non capisco tutto questo hype #PechinoExpress", "likes": 65, "sentiment": "negativo"},

    # Neutri
    {"text": "Stasera parte Pechino Express, vediamo come va #PechinoExpress", "likes": 45, "sentiment": "neutro"},
    {"text": "Chi sta guardando Pechino Express in questo momento? #PechinoExpress2026", "likes": 112, "sentiment": "neutro"},
    {"text": "Terza puntata di Pechino Express, già eliminati in 4 #PechinoExpress", "likes": 67, "sentiment": "neutro"},
    {"text": "Il percorso di quest'anno passa per 5 paesi diversi #PechinoExpress", "likes": 88, "sentiment": "neutro"},
    {"text": "Recap della puntata di stasera: eliminata la coppia X #PechinoExpress2026", "likes": 54, "sentiment": "neutro"},
    {"text": "Pechino Express alle 21:15 su Sky Uno #PechinoExpress", "likes": 33, "sentiment": "neutro"},
    {"text": "Quante coppie sono rimaste? #PechinoExpress", "likes": 41, "sentiment": "neutro"},
]

def generate_mock_data(hashtag: str = "#PechinoExpress", n: int = 50) -> pd.DataFrame:
    """Genera dati mock realistici per l'hashtag specificato."""
    base_time = datetime.now() - timedelta(hours=2)
    rows = []

    for i in range(n):
        tweet = random.choice(MOCK_TWEETS).copy()
        tweet["hashtag"] = hashtag
        tweet["timestamp"] = base_time + timedelta(minutes=random.randint(0, 120))
        tweet["likes"] = tweet["likes"] + random.randint(-20, 50)
        tweet["retweets"] = random.randint(0, tweet["likes"] // 3)
        tweet["username"] = f"utente_{random.randint(1000, 9999)}"
        rows.append(tweet)

    df = pd.DataFrame(rows)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df
