import requests
from bs4 import BeautifulSoup

query = st.text_input("📰 Въведи тема, която те интересува:", "AI investing")
search_url = f"https://www.google.com/search?q={query}+site:reuters.com+OR+site:finance.yahoo.com+OR+site:marketwatch.com&hl=en"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(search_url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

results = []
for g in soup.find_all('div', class_='tF2Cxc'):
    title = g.find('h3')
    link = g.find('a')
    snippet = g.find('div', class_='VwiC3b')
    if title and link and snippet:
        results.append({
            "title": title.text,
            "link": link['href'],
            "snippet": snippet.text
        })
    else:
        st.warning("Няма резултати. Пробвай друга ключова дума.")

st.caption("Made with ☕ and sarcasm by Shadow & James")
