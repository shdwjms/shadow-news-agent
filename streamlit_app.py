# Shadow Intel Agent - Streamlit App
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

# Заглавия
st.title("🕵️ Shadow Intel Agent")
st.subheader("📰 AI & Tech Intelligence Gathering")

# Session state инициализация
if 'search_count' not in st.session_state:
    st.session_state.search_count = 0
if 'last_search_time' not in st.session_state:
    st.session_state.last_search_time = 0

# Избор на тема
query = st.selectbox(
    "📰 Избери тема, която те интересува:",
    ["AI investing", "AI market", "AI stocks", "Nvidia", "OpenAI", "ChatGPT", "Tesla AI"]
)

# Проверка за rate limiting
current_time = time.time()
time_since_last = current_time - st.session_state.last_search_time
min_wait_time = 30  # секунди между заявки

search_disabled = time_since_last < min_wait_time and st.session_state.search_count > 0

if search_disabled:
    remaining_time = int(min_wait_time - time_since_last)
    st.warning(f"⏳ Изчакай {remaining_time} секунди преди следващото търсене...")

# Бутон за търсене
if st.button("🔍 Започни търсенето", disabled=search_disabled):
    st.session_state.search_count += 1
    st.session_state.last_search_time = current_time
    
    # Показване на статистика за заявките
    if st.session_state.search_count > 2:
        st.info(f"🔄 Това е твоята {st.session_state.search_count}-та заявка. При блокиране опитай след 5 минути.")
    
    with st.spinner("Събирам разузнавателна информация... 🕵️"):
        try:
            # Ротиране на User-Agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            ]
            
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive"
            }
            
            # DuckDuckGo търсене
            search_url = f"https://duckduckgo.com/html/?q={query}+site:reuters.com+OR+site:finance.yahoo.com+OR+site:marketwatch.com"
            
            # Пауза за избягване на блокиране
            delay = random.uniform(2, 5)
            time.sleep(delay)
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            # Парсене на резултатите
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
                
                for i, result in enumerate(results[:10]):
                    with st.expander(f"📰 {result['title'][:80]}..."):
                        st.write(f"**Заглавие:** {result['title']}")
                        st.write(f"**Описание:** {result['snippet']}")
                        st.write(f"**Линк:** [{result['link']}]({result['link']})")
                        st.divider()
            else:
                st.warning("⚠️ Няма намерени резултати.")
                st.info("💡 Възможно е сайтът да блокира заявките. Опитай след 30 минути.")
                
        except requests.exceptions.RequestException as e:
            st.error("❌ Грешка при заявката")
            st.error("🚫 Вероятна причина: Сайтът блокира заявките ти")
            
            with st.expander("🛠️ Решения"):
                st.markdown("""
                1. ⏰ Изчакай 30+ минути
                2. 🔄 Рестартирай приложението  
                3. 🌐 Използвай VPN
                4. 🔗 Използвай директните линкове
                """)
                
        except Exception as e:
            st.error(f"❌ Неочаквана грешка: {str(e)}")

# Reset бутон
if st.session_state.search_count > 0:
    if st.button("🔄 Нулирай брояча"):
        st.session_state.search_count = 0
        st.session_state.last_search_time = 0
        st.rerun()

# Директни линкове
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
    st.markdown("- [Bloomberg Tech](https://www.bloomberg.com/technology)")

# Footer
st.divider()
st.caption("Made with ☕ and sarcasm by Shadow & James | 🔥 Powered by Streamlit")

# Sidebar
with st.sidebar:
    st.header("ℹ️ Как работи?")
    st.write("""
    1. 🎯 Избери тема
    2. 🔍 Натисни бутона
    3. 📊 Разгледай резултатите
    4. 🔗 Използвай директните линкове
    """)
    
    st.header("⚠️ Забележки")
    st.write("""
    - Максимум 2-3 заявки на час
    - При блокиране изчакай 30+ минути
    - Директните линкове винаги работят
    """)
    
    # Статистика
    if st.session_state.search_count > 0:
        st.header("📊 Статистика")
        st.metric("Направени заявки", st.session_state.search_count)
        
        if st.session_state.search_count > 3:
            st.warning("⚠️ Много заявки!")
        
        minutes_passed = int((time.time() - st.session_state.last_search_time) / 60)
        st.metric("Минути от последна заявка", minutes_passed)
