import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.mock_tweets import generate_mock_data
from utils.sentiment import analyze_dataframe, get_top_tweets, get_sentiment_over_time, get_word_frequency

st.set_page_config(page_title="Sentiment Pechino Express", page_icon="✈️", layout="wide")

st.markdown("""
<style>
    .tweet-card { background: #1e1e2e; border-radius: 10px; padding: 15px; margin: 8px 0; border-left: 4px solid; }
    .title-gradient { background: linear-gradient(90deg, #ff6b35, #f7c59f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5em; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✈️ Configurazione")
    hashtag = st.selectbox("📌 Hashtag", ["#PechinoExpress", "#PechinoExpress2026", "#PechinoExpress25", "Personalizzato..."])
    if hashtag == "Personalizzato...":
        hashtag = st.text_input("Inserisci hashtag:", value="#PechinoExpress")
    n_tweets = st.slider("📊 Numero di tweet", 20, 200, 80, step=10)
    use_mock = st.radio("🔌 Fonte dati", ["📦 Dati demo (mock)", "🔑 API X (richiede chiave)"])
    if use_mock == "🔑 API X (richiede chiave)":
        api_key = st.text_input("Bearer Token X API", type="password")
        st.info("💡 Ottieni le credenziali su developer.x.com")
    st.divider()
    if st.button("🔄 Aggiorna dati", use_container_width=True, type="primary"):
        st.cache_data.clear()
    st.caption(f"Aggiornato: {datetime.now().strftime('%H:%M:%S')}")

@st.cache_data(ttl=60)
def load_data(hashtag, n):
    df = generate_mock_data(hashtag=hashtag, n=n)
    df = analyze_dataframe(df)
    df["sentiment"] = pd.Series([str(x).strip().lower() for x in df["sentiment"]], index=df.index)
    return df

with st.spinner("🔍 Analisi in corso..."):
    df = load_data(hashtag, n_tweets)

st.markdown('<div class="title-gradient">✈️ Sentiment Analyzer</div>', unsafe_allow_html=True)
st.markdown(f"### Analisi tweet per **{hashtag}** • {len(df)} tweet analizzati")
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
