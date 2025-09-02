# ✅ Shadow Intel Agent - Streamlit App (v2 with GNews API)

import streamlit as st
import requests

# -----------------------
# 🔧 Config
# -----------------------
API_KEY = "724ee3f8ef1541ab470ba9280bf3ee82"
API_URL = "https://gnews.io/api/v4/search"

# -----------------------
# 🌑 UI
# -----------------------
st.set_page_config(page_title="Shadow News Agent", layout="wide")
st.title("🕵️‍♀️ Shadow Intel Agent – GNews Edition")
st.caption("Извличане и анализ на реални новини от сигурен източник.")

query = st.selectbox(
    "📰 Избери тема, която те интересува:",
    ["AI investing", "AI market", "AI stocks", "Nvidia", "OpenAI"]
)

if query:
    params = {
        "q": query,
        "lang": "en",
        "token": API_KEY,
        "max": 10,
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    articles = data.get("articles", [])

    if articles:
        for i, article in enumerate(articles, 1):
            st.markdown(f"**{i}. [{article['title']}]({article['url']})**")
            st.caption(article['publishedAt'])
            st.write(article['description'])
            st.markdown("---")
    else:
        st.warning("Няма резултати. Пробвай друга ключова дума.")

st.caption("Made with ☕ and sarcasm by Shadow & James")
