# Shadow Intel Agent - NewsAPI Version (modified with new UI styles)
import streamlit as st
import requests
import json
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Shadow Intel Agent",
    page_icon="🕵️",
    layout="wide"
)

# -------------------------------------------------------------
# Custom styling
#
# Define CSS variables and fonts to match the requested palette:
# - Primary color: Shadow Violet (#5F4B8B)
# - Background: #F2F4F7
# - Accent colors: Matcha Green (#B7DD79) or Butter Yellow (#FFD56B)
# - Fonts: Palettone for headings (with sensible fallback), Raleway/Inter for body text
# - Sidebar with a translucent blur
# - Rounded buttons with emoji labels
#
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Raleway:wght@400;600;700&display=swap');

/* Colour palette variables */
:root {
  --primary-color: #5F4B8B;
  --background-color: #F2F4F7;
  --accent-green: #B7DD79;
  --accent-yellow: #FFD56B;
}

/* Base styles */
html, body, [class*="css"]  {
  background-color: var(--background-color) !important;
  font-family: 'Inter', 'Raleway', sans-serif;
}

h1, h2, h3, h4 {
  font-family: 'Palettone', 'Inter', sans-serif;
  color: var(--primary-color);
}

/* Style the Streamlit buttons */
.stButton > button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-family: 'Inter', 'Raleway', sans-serif;
}

/* Sidebar styling: translucent with blur */
div[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.6) !important;
  backdrop-filter: blur(8px);
}
</style>
"""

# Inject custom CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------------------------------------------
# Titles and headers
st.title("🕵️ Shadow Intel Agent")
st.subheader("📰 AI & Tech Intelligence Gathering")

# Tagline conveying personality
st.caption("AI, но с характер.")

# Session state for counting searches
if 'search_count' not in st.session_state:
    st.session_state.search_count = 0

# NewsAPI key (hard-coded for demonstration)
NEWSAPI_KEY = "cdd83a93db6344bc95c7d5eedd117c02"

# Topic selection
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

# Filters
col1, col2 = st.columns(2)
with col1:
    days_back = st.slider("📅 Новини за последните дни:", 1, 30, 7)
with col2:
    language = st.selectbox("🌍 Език:", ["en", "bg"], index=0)

# Primary API method
def search_with_newsapi(api_key, query, days_back, language):
    """
    Fetch articles from NewsAPI based on the query and filters.
    """
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

# Alternative method without API
def search_alternative():
    """
    Use public RSS feeds when no API key is provided.
    """
    try:
        # TechCrunch RSS for AI news
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

                for entry in feed.entries[:5]:  # First 5 from each feed
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

# Search button
if st.button("🔍 Decode News"):
    st.session_state.search_count += 1

    with st.spinner("Търся актуални новини... 📰"):

        if NEWSAPI_KEY:
            # Use NewsAPI
            data = search_with_newsapi(NEWSAPI_KEY, query, days_back, language)
        else:
            # Use RSS alternative
            data = search_alternative()

        if data and data.get('articles'):
            articles = data['articles']
            total = data.get('totalResults', len(articles))

            st.success(f"✅ Намерени са {len(articles)} новини от общо {total}")

            # Display results
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

# Statistics
if st.session_state.search_count > 0:
    st.info(f"📊 Направени заявки тази сесия: {st.session_state.search_count}")

    if NEWSAPI_KEY and st.session_state.search_count > 80:
        st.warning("⚠️ Близо до лимита от 100 заявки/ден!")

# Direct links (backup)
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
st.caption("Made with ☻ and sarcasm by Shadow & James")

# Sidebar information with blur and translucent styling (CSS applied above)
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