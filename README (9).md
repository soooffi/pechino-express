# ✈️ Sentiment Analyzer — Pechino Express

> Dashboard interattiva per analizzare il sentiment dei tweet su **#PechinoExpress** in tempo reale.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Screenshot

> Dashboard con grafici interattivi, top tweet per like e analisi temporale del sentiment.

---

## 🚀 Funzionalità

- 🔎 **Ricerca per hashtag** — analizza qualsiasi `#hashtag` di X/Twitter
- 😊😠😐 **Sentiment Analysis** — classifica ogni tweet in Positivo / Negativo / Neutro
- ❤️ **Top tweet per like** — mostra i commenti più apprezzati dal pubblico
- 📊 **Dashboard visuale** — grafici a torta, trend temporale, parole più usate
- 📈 **Andamento live** — come cambia il sentiment durante la serata
- ⬇️ **Export CSV** — scarica tutti i dati analizzati
- 🔌 **Modalità demo** — funziona senza API key con dati mock realistici

---

## 🛠️ Stack Tecnologico

| Tool | Uso |
|------|-----|
| `Streamlit` | UI e dashboard interattiva |
| `TextBlob` | NLP e sentiment analysis |
| `Plotly` | Grafici interattivi |
| `Pandas` | Manipolazione dati |
| `X API v2` | Raccolta tweet (opzionale) |

---

## ⚙️ Installazione

```bash
# 1. Clona il repository
git clone https://github.com/tuo-username/sentiment-pechino-express.git
cd sentiment-pechino-express

# 2. Installa le dipendenze
pip install -r requirements.txt

# 3. Avvia l'app
streamlit run app.py
```

L'app si aprirà automaticamente su `http://localhost:8501`

---

## 🔑 Configurazione API X (opzionale)

Per usare dati reali da X/Twitter:

1. Crea un account su [developer.x.com](https://developer.x.com)
2. Crea un nuovo progetto e ottieni il **Bearer Token**
3. Incolla il token nella sidebar dell'app

> ℹ️ Senza API key, l'app funziona con dati demo realistici.

---

## 📁 Struttura Progetto

```
sentiment-pechino-express/
├── app.py                  # App principale Streamlit
├── requirements.txt        # Dipendenze Python
├── data/
│   └── mock_tweets.py      # Generatore dati demo
└── utils/
    └── sentiment.py        # Logica NLP e analisi
```

---

## 🗺️ Roadmap

- [ ] Integrazione API X v2 in tempo reale
- [ ] Supporto multi-hashtag simultaneo
- [ ] Notifiche push quando il sentiment crolla
- [ ] Confronto tra puntate diverse
- [ ] Deploy su Streamlit Cloud

---

## 📄 Licenza

MIT License — libero di usare, modificare e distribuire.

---

*Progetto realizzato con ❤️ per gli appassionati di Pechino Express e NLP*
