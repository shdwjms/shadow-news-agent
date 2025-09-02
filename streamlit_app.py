# Shadow Intel Agent - NewsAPI Version
import streamlit as st
import requests
import json
from datetime import datetime, timedelta

# Конфигуриране на страницата
st.set_page_config(
    page_title="Shadow Intel Agent",
    page_icon="🕵️",
    layout="wide"
)

# Заглавия
st.title("🕵️ Shadow Intel Agent")
st.subheader("📰 AI & Tech Intelligence Gathering")

# Session state
if 'search_count' not in st.session_state:
    st.session_state.search_count = 0

# NewsAPI ключ (вмъкнат директно)
NEWSAPI_KEY = "cdd83a93db6344bc95c7d5eedd117c02"
    
    st.warning("⚠️ Без API ключ ще използваме алтернативен метод (по-ограничен)")

# Избор на тема
query_options = {
    "AI investing": "artificial intelligence investing OR AI stocks",
    "AI market": "artificial intelligence market trends", 
    "AI stocks": "AI stocks OR artificial intelligence companies",
    "Nvidia": "Nvidia OR NVDA stock",
    "OpenAI": "OpenAI OR ChatGPT",
    "ChatGPT": "ChatGPT OR OpenAI",
    "Tesla AI": "Tesla artificial intelligence OR Tesla FSD"
}

selected_topic = st.selectbox(
    "📰 Избери тема:",
    list(query_options.keys())
)

query = query_options[selected_topic]

# Филтри
col1, col2 = st.columns(2)
with col1:
    days_back = st.slider("📅 Новини за последните дни:", 1, 30, 7)
with col2:
    language = st.selectbox("🌍 Език:", ["en", "bg"], index=0)

# Основен API метод
def search_with_newsapi(api_key, query, days_back, language):
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'from': from_date,
        'language': language,
        'sortBy': 'relevancy',
        'pageSize': 20,
        'apiKey': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API грешка: {str(e)}")
        return None

# Алтернативен метод без API
def search_alternative():
    """Използва публични RSS feeds"""
    try:
        # TechCrunch RSS за AI новини
        rss_urls = {
            "TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "VentureBeat": "https://feeds.feedburner.com/venturebeat/SZYF",
            "AI News": "https://www.artificialintelligence-news.com/feed/"
        }
        
        st.info("🔄 Използвам алтернативни източници (RSS feeds)...")
        
        results = []
        for source, url in rss_urls.items():
            try:
                import feedparser
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:5]:  # Първите 5 от всеки feed
                    results.append({
                        'title': entry.title,
                        'description': entry.get('summary', 'Няма описание'),
                        'url': entry.link,
                        'source': source,
                        'publishedAt': entry.get('published', 'Неизвестна дата')
                    })
            except:
                continue
                
        return {'articles': results, 'totalResults': len(results)}
        
    except ImportError:
        st.error("❌ За алтернативния метод е нужен feedparser: pip install feedparser")
        return None

# Бутон за търсене
if st.button("🔍 Започни търсенето"):
    st.session_state.search_count += 1
    
    with st.spinner("Търся актуални новини... 📰"):
        
        if NEWSAPI_KEY:
            # Използваме NewsAPI
            data = search_with_newsapi(NEWSAPI_KEY, query, days_back, language)
        else:
            # Алтернативен метод
            data = search_alternative()
        
        if data and data.get('articles'):
            articles = data['articles']
            total = data.get('totalResults', len(articles))
            
            st.success(f"✅ Намерени са {len(articles)} новини от общо {total}")
            
            # Показване на резултатите
            for i, article in enumerate(articles):
                with st.expander(f"📰 {article['title'][:80]}..."):
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### {article['title']}")
                        st.write(article.get('description', 'Няма описание'))
                        
                        if article.get('publishedAt'):
                            try:
                                pub_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
                                st.caption(f"📅 {pub_date.strftime('%d.%m.%Y %H:%M')}")
                            except:
                                st.caption(f"📅 {article['publishedAt']}")
                    
                    with col2:
                        if article.get('urlToImage'):
                            try:
                                st.image(article['urlToImage'], width=150)
                            except:
                                st.write("🖼️ Изображение недостъпно")
                        
                        st.markdown(f"**Източник:** {article.get('source', {}).get('name', 'Неизвестен')}")
                    
                    st.markdown(f"🔗 [Прочети пълната статия]({article['url']})")
                    st.divider()
        else:
            st.warning("⚠️ Няма намерени резултати")
            if not NEWSAPI_KEY:
                st.info("💡 Добави API ключ за по-добри резултати!")

# Статистика
if st.session_state.search_count > 0:
    st.info(f"📊 Направени заявки тази сесия: {st.session_state.search_count}")
    
    if NEWSAPI_KEY and st.session_state.search_count > 80:
        st.warning("⚠️ Близо до лимита от 100 заявки/ден!")

# Директни линкове (като backup)
st.divider()
st.subheader("🔗 Директни източници (винаги работят)")

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
    st.markdown("- [TechCrunch AI](https://techcrunch.com/category/artificial-intelligence/)")

with col3:
    st.markdown("### 💼 Инвестиции")
    st.markdown("- [Seeking Alpha](https://seekingalpha.com)")
    st.markdown("- [Benzinga](https://www.benzinga.com)")
    st.markdown("- [Bloomberg Tech](https://www.bloomberg.com/technology)")

# Footer
st.divider()
st.caption("Made with ☕ and sarcasm by Shadow & James | 🚀 Powered by NewsAPI + Streamlit")

# Sidebar с информация
with st.sidebar:
    st.header("🆕 Нова версия с NewsAPI!")
    st.success("✅ Няма блокирания!")
    st.success("✅ 100 безплатни заявки/ден")
    st.success("✅ Структурирани данни")
    st.success("✅ Филтри по дата и език")
    
    st.header("ℹ️ Как работи:")
    st.write("""
    1. 🔑 Въведи API ключ (еднократно)
    2. 🎯 Избери тема
    3. 📅 Настрой филтрите
    4. 🔍 Натисни търсене
    5. 📰 Разгледай новините!
    """)
    
    st.header("💡 Без API ключ?")
    st.write("Ще използваме RSS feeds, но с по-ограничени резултати.")
    
    if st.button("🔄 Нулирай брояча"):
        st.session_state.search_count = 0
        st.rerun()
