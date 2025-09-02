# Бутон за reset на брояча
if st.session_state.search_count > 0:
    if st.button("🔄 Нулирай брояча на заявките"):
        st.session_state.search_count = 0
        st.session_state.last_search_time = 0
        st.rerun()# ✅ Shadow Intel Agent - Streamlit App (Fixed Version)

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

# Session state за проследяване на заявките
if 'search_count' not in st.session_state:
    st.session_state.search_count = 0
if 'last_search_time' not in st.session_state:
    st.session_state.last_search_time = 0

# Проверка за rate limiting
current_time = time.time()
time_since_last = current_time - st.session_state.last_search_time
min_wait_time = 30  # секundi между заявки

# Бутон за търсене с rate limiting
search_disabled = time_since_last < min_wait_time and st.session_state.search_count > 0

if search_disabled:
    remaining_time = int(min_wait_time - time_since_last)
    st.warning(f"⏳ Изчакай {remaining_time} секунди преди следващото търсене...")
    
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
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
            ]
            
            headers = {
                "User-Agent": random.choice(user_agents),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none"
            }
            
            # Алтернативен подход - използване на DuckDuckGo вместо Google
            search_url = f"https://duckduckgo.com/html/?q={query}+site:reuters.com+OR+site:finance.yahoo.com+OR+site:marketwatch.com"
            
            # По-дълго закъснение за избягване на блокиране
            delay = random.uniform(3, 8) if st.session_state.search_count > 2 else random.uniform(1, 3)
            time.sleep(delay)
            
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
            st.error("🚫 **Вероятна причина:** Сайтът блокира заявките ти")
            
            with st.expander("🛠️ Решения за блокирането"):
                st.markdown("""
                **Опитай следните методи:**
                1. ⏰ **Изчакай 5-10 минути** преди следващо търсене
                2. 🔄 **Рестартирай приложението** (F5)
                3. 🌐 **Използвай VPN** за смяна на IP адреса
                4. 📱 **Опитай от различно устройство/мрежа**
                5. 🔗 **Използвай директните линкове** по-долу
                """)
                
        except Exception as e:
            st.error(f"❌ Неочаквана грешка: {str(e)}")
            
# Тест секция за проверка на блокиране
st.divider()
st.subheader("🧪 Диагностика на блокиране")

col1, col2 = st.columns(2)

with col1:
    if st.button("🌐 Тестов ping"):
        try:
            test_response = requests.get("https://httpbin.org/user-agent", timeout=5)
            st.success("✅ Интернет връзката работи")
            st.json(test_response.json())
        except:
            st.error("❌ Проблем с интернет връзката")

with col2:
    if st.button("🔍 Тест DuckDuckGo"):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            test_url = "https://duckduckgo.com/html/?q=test"
            response = requests.get(test_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                st.success(f"✅ DuckDuckGo отговаря (Status: {response.status_code})")
                if "blocked" in response.text.lower() or "captcha" in response.text.lower():
                    st.warning("⚠️ Възможно блокиране детектирано")
                else:
                    st.info("🟢 Изглежда не си блокиран")
            else:
                st.error(f"❌ Необичаен отговор: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ Грешка при тестването: {str(e)}")

# Съвети за по-бързо възстановяване
with st.expander("⚡ Как да се възстановиш по-бързо?"):
    st.markdown("""
    ### 🚀 Бързи решения:
    1. **🔄 Смени браузъра** - Chrome → Firefox → Edge
    2. **📱 Опитай от телефона** (различна мрежа)
    3. **🏠 Смени WiFi мрежата** (мобилни данни)
    4. **🌐 VPN** - промяна на местоположението
    5. **⏰ Изчакай 30+ минути** и опитай отново
    
    ### 🔧 Технически трикове:
    - Изтрий cookies и cache
    - Рестартирай рутера (нов IP от ISP)
    - Използвай Incognito/Private режим
    """)

# Real-time статус
st.markdown("### 📊 Текущ статус:")
status_cols = st.columns(4)
with status_cols[0]:
    st.metric("Заявки направени", st.session_state.search_count)
with status_cols[1]:
    if st.session_state.search_count == 0:
        st.metric("Риск ниво", "🟢 Ниско")
    elif st.session_state.search_count < 3:
        st.metric("Риск ниво", "🟡 Средно") 
    else:
        st.metric("Риск ниво", "🔴 Високо")
with status_cols[2]:
    minutes_passed = int((time.time() - st.session_state.last_search_time) / 60) if st.session_state.last_search_time > 0 else 0
    st.metric("Минути от последна заявка", minutes_passed)
with status_cols[3]:
    if minutes_passed > 30:
        st.metric("Препоръка", "✅ Опитай сега")
    else:
        st.metric("Препоръка", f"⏳ Изчакай още {30-minutes_passed}м")

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
    
    # Статистика за заявките
    if st.session_state.search_count > 0:
        st.header("📊 Статистика")
        st.metric("Направени заявки", st.session_state.search_count)
        if st.session_state.search_count > 3:
            st.warning("⚠️ Много заявки! Възможно блокиране.")
