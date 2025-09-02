# ✅ Shadow Intel Agent - Streamlit App (Fixed Version)

import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random

# Конфигуриране на страницата
st.set_page_config(
    page_title="Shadow Intel Agent",
    page_icon="🕵️",
    layout="wide"
)

st.title("🕵️ Shadow Intel Agent")
st.subheader("📰 AI & Tech Intelligence Gathering")

# Избор на тема
query = st.selectbox(
    "📰 Избери тема, която те интересува:",
    ["AI investing", "AI market", "AI stocks", "Nvidia", "OpenAI", "ChatGPT", "Tesla AI"]
)

# Бутон за търсене
if st.button("🔍 Започни търсенето"):
    with st.spinner("Събирам разузнавателна информация... 🕵️"):
        try:
            # По-добри headers за избягване на блокиране
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive"
            }
            
            # Алтернативен подход - използване на DuckDuckGo вместо Google
            search_url = f"https://duckduckgo.com/html/?q={query}+site:reuters.com+OR+site:finance.yahoo.com+OR+site:marketwatch.com"
            
            # Добавяне на случайно закъснение
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            # Търсене за DuckDuckGo резултати
            for result in soup.find_all('div', class_='result'):
                title_elem = result.find('h2')
                link_elem = result.find('a', class_='result__url')
                snippet_elem = result.find('div', class_='result__snippet')
                
                if title_elem and link_elem:
                    title = title_elem.get_text().strip()
                    link = link_elem.get('href', '')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else "Няма описание"
                    
                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
            
            # Показване на резултатите
            if results:
                st.success(f"✅ Намерени са {len(results)} резултата!")
                
                for i, result in enumerate(results[:10]):  # Показваме само първите 10
                    with st.expander(f"📰 {result['title'][:80]}..."):
                        st.write(f"**Заглавие:** {result['title']}")
                        st.write(f"**Описание:** {result['snippet']}")
                        st.write(f"**Линк:** [{result['link']}]({result['link']})")
                        st.divider()
            else:
                st.warning("⚠️ Няма намерени резултати. Опитай с друга ключова дума.")
                st.info("💡 **Съвет:** Възможно е сайтът да блокира заявките. Опитай след малко.")
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Грешка при заявката: {str(e)}")
            st.info("💡 **Алтернатива:** Опитай директно в браузъра или използвай VPN.")
            
        except Exception as e:
            st.error(f"❌ Неочаквана грешка: {str(e)}")

# Алтернативен раздел с директни линкове
st.divider()
st.subheader("🔗 Директни източници")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Финанси")
    st.markdown("- [Yahoo Finance](https://finance.yahoo.com)")
    st.markdown("- [MarketWatch](https://www.marketwatch.com)")
    st.markdown("- [Reuters](https://www.reuters.com)")

with col2:
    st.markdown("### 🤖 AI Новини")
    st.markdown("- [VentureBeat AI](https://venturebeat.com/ai/)")
    st.markdown("- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence)")
    st.markdown("- [AI News](https://www.artificialintelligence-news.com/)")

with col3:
    st.markdown("### 💼 Инвестиции")
    st.markdown("- [Seeking Alpha](https://seekingalpha.com)")
    st.markdown("- [TechCrunch](https://techcrunch.com)")
    st.markdown("- [The Information](https://www.theinformation.com)")

# Footer
st.divider()
st.caption("Made with ☕ and sarcasm by Shadow & James | 🔥 Powered by Streamlit")

# Странична лента с информация
with st.sidebar:
    st.header("ℹ️ Как работи?")
    st.write("""
    1. 🎯 Избери тема от менюто
    2. 🔍 Натисни 'Започни търсенето'
    3. 📊 Разгледай резултатите
    4. 🔗 Използвай директните линкове за повече информация
    """)
    
    st.header("⚠️ Забележки")
    st.write("""
    - Някои сайтове могат да блокират автоматизирани заявки
    - За най-актуални данни използвай директните линкове
    - Ако има грешки, опитай след няколко минути
    """)
