import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.mock_tweets import generate_mock_data
from data.twitter_api import get_tweets_by_hashtag
from utils.sentiment import analyze_dataframe, get_top_tweets, get_sentiment_over_time, get_word_frequency

st.set_page_config(page_title="Sentiment Pechino Express", page_icon="✈️", layout="wide")

def _get_app_styles():
    return """
<style>
    body, .stApp, .main, .block-container, .css-18e3th9, .css-12oz5g7 {
        background: #0b0c10 !important;
        color: #f1f1f1 !important;
    }
    .app-header {
        width: 100%;
        margin-bottom: 0px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #0b0c10;
        border-radius: 12px;
        padding: 8px 18px 0px 18px;
    }
    div[data-testid="stMarkdownContainer"] + div[data-testid="stMarkdownContainer"] {
        margin-top: -1rem;
    }
    .block-container {
        padding-top: 1rem !important;
        gap: 0 !important;
    }
    section.main > div > div:first-child {
        gap: 0 !important;
    }
    .header-brand-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        width: 100%;
    }
    .header-logo {
        width: min(40vw, 220px);
        height: min(40vw, 220px);
        object-fit: contain;
    }
    .header-logo-x {
        width: min(20vw, 110px);
        height: min(20vw, 110px);
        object-fit: contain;
        margin-left: 24px;
    }
    .header-collab {
        font-size: clamp(18px, 2.5vw, 32px);
        font-weight: 900;
        font-family: 'Georgia', 'Times New Roman', serif;
        background: linear-gradient(90deg, #C9933A, #F5D27A, #C9933A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.06em;
        line-height: 1;
    }
    .stButton>button, .stTextInput>div>div>input, .stSlider>div>div>div {
        background-color: rgba(20, 22, 32, 0.95) !important;
        color: #f1f1f1 !important;
    }
    div[data-testid="metric"] span, div[data-testid="metric"] div {
        color: #f1f1f1 !important;
    }
    .tweet-card {
        background: rgba(30, 32, 44, 0.85);
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid;
    }
</style>
"""

def _get_header_html():
    base_dir = os.path.dirname(__file__)
    pechino_logo_path = os.path.join(base_dir, "assets", "pechino_logo.png")
    x_logo_path = os.path.join(base_dir, "2150506.jpeg")

    if not os.path.exists(pechino_logo_path) or not os.path.exists(x_logo_path):
        return "<div class='app-header'></div>"

    with open(pechino_logo_path, "rb") as f:
        pechino_encoded = base64.b64encode(f.read()).decode("utf-8")
    with open(x_logo_path, "rb") as f:
        x_encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"""
    <div class='app-header'>
        <div class='header-brand-row'>
            <img class='header-logo' src='data:image/png;base64,{pechino_encoded}' alt='Pechino Express logo' />
            <span class='header-collab'>X</span>
            <img class='header-logo-x' src='data:image/jpeg;base64,{x_encoded}' alt='X logo' />
        </div>
    </div>
    """

def _build_gallery_html(folder, title):
    dirpath = os.path.join(os.path.dirname(__file__), folder)
    if not os.path.exists(dirpath):
        return ""
    files = sorted(f for f in os.listdir(dirpath) if f.lower().endswith((".jpg", ".jpeg", ".png", ".avif", ".webp")))
    if not files:
        return ""
    cards = ""
    for fname in files:
        name = os.path.splitext(fname)[0].replace("-", " ").replace("_", " ").upper()
        ext = os.path.splitext(fname)[1].lower().lstrip(".")
        mime = "jpeg" if ext in ("jpg", "jpeg") else ("png" if ext == "png" else ("webp" if ext == "webp" else ext))
        with open(os.path.join(dirpath, fname), "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        cards += f"""
        <div style="display:flex;flex-direction:column;align-items:center;min-width:160px;max-width:160px;">
            <img src="data:image/{mime};base64,{encoded}"
                 style="width:150px;height:150px;object-fit:cover;border-radius:12px;border:2px solid #C9933A;" />
            <span style="
                margin-top:8px;
                font-family:'Georgia','Times New Roman',serif;
                font-weight:700;
                font-size:13px;
                color:#F5D27A;
                text-align:center;
                letter-spacing:0.05em;
                line-height:1.3;
            ">{name}</span>
        </div>"""
    return f"""
    <div style="margin:4px 0 8px 0;">
        <div style="
            font-family:'Georgia','Times New Roman',serif;
            font-size:clamp(16px,2vw,24px);
            font-weight:900;
            background:linear-gradient(90deg,#C9933A,#F5D27A,#C9933A);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            background-clip:text;
            letter-spacing:0.1em;
            text-transform:uppercase;
            text-align:center;
            margin-bottom:22px;
            margin-top:14px;
        ">{title}</div>
        <div style="
            display:flex;
            flex-direction:row;
            gap:18px;
            overflow-x:auto;
            padding-bottom:10px;
            scrollbar-width:thin;
            scrollbar-color:#C9933A #1a1a2e;
        ">
            {cards}
        </div>
    </div>
    """

def _get_coppie_html():
    return _build_gallery_html("coppie", "LE COPPIE")

st.markdown(_get_app_styles(), unsafe_allow_html=True)
st.markdown(_get_header_html(), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✈️ Configurazione")
    hashtag = st.selectbox("📌 Hashtag", ["#PechinoExpress", "#PechinoExpress2026", "#PechinoExpress25", "Personalizzato..."])
    if hashtag == "Personalizzato...":
        hashtag = st.text_input("Inserisci hashtag:", value="#PechinoExpress")
    n_tweets = st.slider("📊 Numero di tweet", 20, 100, 80, step=10)
    use_api = st.radio("🔌 Fonte dati", ["📦 Dati demo (mock)", "🔑 API X (reale)"])
    st.divider()
    if st.button("🔄 Aggiorna dati", use_container_width=True, type="primary"):
        st.cache_data.clear()
    st.caption(f"Aggiornato: {datetime.now().strftime('%H:%M:%S')}")

@st.cache_data(ttl=60)
def load_mock(hashtag, n):
    df = generate_mock_data(hashtag=hashtag, n=n)
    df = analyze_dataframe(df)
    df["sentiment"] = pd.Series([str(x).strip().lower() for x in df["sentiment"]], index=df.index)
    return df

@st.cache_data(ttl=60)
def load_real(hashtag, n):
    df = get_tweets_by_hashtag(hashtag=hashtag, max_results=n)
    if df.empty:
        return df
    df = analyze_dataframe(df)
    df["sentiment"] = pd.Series([str(x).strip().lower() for x in df["sentiment"]], index=df.index)
    return df

with st.spinner("🔍 Analisi in corso..."):
    if use_api == "🔑 API X (reale)":
        df = load_real(hashtag, n_tweets)
        if df.empty:
            st.warning("⚠️ Nessun tweet trovato dall'API. Uso dati demo.")
            df = load_mock(hashtag, n_tweets)
    else:
        df = load_mock(hashtag, n_tweets)

fonte = "🔑 API X reale" if use_api == "🔑 API X (reale)" else "📦 Demo"
st.markdown("""
<div style="
    text-align: center;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: clamp(22px, 3.5vw, 40px);
    font-weight: 900;
    color: #C9933A;
    background: linear-gradient(90deg, #C9933A, #F5D27A, #C9933A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 0px 0 10px 0;
    line-height: 1.2;
">I TWEET MIGLIORI DI PECHINO EXPRESS 2026</div>
<hr style="border:none;border-top:1px solid #3a3a4a;margin:30px auto 20px auto;width:60%;" />
""", unsafe_allow_html=True)
full_gallery = f"""<html><body style="background:#0b0c10;margin:0;padding:0;">{_get_coppie_html()}<div style="display:flex;justify-content:center;"><div style="height:28px;border-top:1px solid #2a2a3a;margin:10px 0;width:60%;"></div></div>{_build_gallery_html('conduttori', 'I CONDUTTORI')}</body></html>"""
components.html(full_gallery, height=560, scrolling=False)
st.divider()

sentiments = [str(x).strip().lower() for x in df["sentiment"]]
pos = sentiments.count("positivo")
neg = sentiments.count("negativo")
neu = sentiments.count("neutro")
total = max(len(sentiments), 1)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("😊 Positivi", pos, f"{pos/total*100:.1f}%")
with col2:
    st.metric("😠 Negativi", neg, f"{neg/total*100:.1f}%", delta_color="inverse")
with col3:
    st.metric("😐 Neutri", neu, f"{neu/total*100:.1f}%")
with col4:
    st.metric("❤️ Like medi", int(df["likes"].mean()))

st.divider()

col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📊 Distribuzione Sentiment")
    fig_pie = px.pie(values=[pos, neg, neu], names=["Positivo 😊", "Negativo 😠", "Neutro 😐"],
                     color_discrete_sequence=["#2ecc71", "#e74c3c", "#95a5a6"], hole=0.4)
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                          legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("📈 Sentiment nel Tempo")
    time_df = get_sentiment_over_time(df)
    fig_line = go.Figure()
    colors = {"positivo": "#2ecc71", "negativo": "#e74c3c", "neutro": "#95a5a6"}
    for s in ["positivo", "negativo", "neutro"]:
        if s in time_df.columns:
            fig_line.add_trace(go.Scatter(x=time_df["time_bucket"], y=time_df[s],
                name=s.capitalize(), line=dict(color=colors[s], width=2.5), fill="tozeroy"))
    fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           font_color="white", xaxis=dict(gridcolor="#333"), yaxis=dict(gridcolor="#333"))
    st.plotly_chart(fig_line, use_container_width=True)

st.subheader("☁️ Parole più usate")
word_freq = get_word_frequency(df, top_n=20)
if word_freq:
    wf_df = pd.DataFrame(list(word_freq.items()), columns=["parola", "frequenza"])
    fig_bar = px.bar(wf_df.sort_values("frequenza", ascending=True).tail(15),
                     x="frequenza", y="parola", orientation="h", color="frequenza",
                     color_continuous_scale=["#3a3a5c", "#ff6b35"])
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", showlegend=False, coloraxis_showscale=False, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.subheader("🏆 Top Tweet per Like")
tab1, tab2, tab3 = st.tabs(["❤️ Tutti", "😊 Più positivi", "😠 Più negativi"])

def render_tweets(tweets_df):
    for _, row in tweets_df.iterrows():
        s = str(row["sentiment"])
        border_color = {"positivo": "#2ecc71", "negativo": "#e74c3c", "neutro": "#95a5a6"}.get(s, "#666")
        st.markdown(f"""
        <div class="tweet-card" style="border-left-color: {border_color}">
            <strong>@{row['username']}</strong> {row.get('emoji', '')}
            <p style="margin: 6px 0 4px 0">{row['text']}</p>
            <small style="color: #aaa">❤️ {row['likes']} like &nbsp; 🔁 {row['retweets']} retweet &nbsp;
            <span style="color:{border_color}">● {s.upper()}</span></small>
        </div>""", unsafe_allow_html=True)

with tab1:
    render_tweets(get_top_tweets(df, n=8))
with tab2:
    render_tweets(get_top_tweets(df, sentiment="positivo", n=5))
with tab3:
    render_tweets(get_top_tweets(df, sentiment="negativo", n=5))

st.divider()
with st.expander("📋 Visualizza tutti i tweet analizzati"):
    display_df = df[["username", "text", "sentiment", "emoji", "score", "likes", "retweets", "timestamp"]].copy()
    display_df["timestamp"] = pd.to_datetime(display_df["timestamp"]).dt.strftime("%H:%M")
    display_df["score"] = display_df["score"].astype(float)
    st.dataframe(display_df, use_container_width=True, hide_index=True,
                 column_config={"score": st.column_config.ProgressColumn("Score", min_value=-1, max_value=1),
                                "likes": st.column_config.NumberColumn("❤️ Like"),
                                "retweets": st.column_config.NumberColumn("🔁 RT")})
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Scarica CSV", csv, "sentiment_pechino.csv", "text/csv")
