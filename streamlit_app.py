import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Shadow News Agent", layout="wide")
st.title("🕵️‍♀️ Shadow Intel Agent – Auto News Scraper")

query = st.text_input("📰 Въведи тема, която те интересува:", "AI investing")

if query:
    url = f"https://www.google.com/search?q={query}+site:reuters.com+OR+site:finance.yahoo.com+OR+site:fool.com+OR+site:seekingalpha.com+OR+site:marketwatch.com&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }

    requests.get(f"https://gnews.io/api/v4/search?q={query}&token=724ee3f8ef1541ab470ba9280bf3ee82&lang=en")
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("a")

    links = []
    for r in results:
        href = r.get("href")
        if href and "reuters.com" in href and "/url?q=" in href:
            link = href.split("/url?q=")[1].split("&")[0]
            if link not in links:
                links.append(link)

    if links:
        for i, link in enumerate(links[:10], 1):
            st.markdown(f"**{i}.** [{link}]({link})")
    else:
        st.warning("Нищо не беше намерено. Пробвай друга ключова дума.")
