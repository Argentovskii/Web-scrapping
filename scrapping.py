import requests
from bs4 import BeautifulSoup
import time

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = "https://habr.com/ru/all/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("article")

for article in articles:
    title_tag = article.find("h2")
    if not title_tag:
        continue

    title = title_tag.text.strip()
    link = "https://habr.com" + title_tag.find("a").get("href")

    time_tag = article.find("time")
    date = time_tag.text.strip() if time_tag else ""

    preview = article.text.lower()

    # сначала проверяем preview
    if any(keyword.lower() in preview for keyword in KEYWORDS):
        print(f"{date} – {title} – {link}")
        continue

    # если не нашли — идём в статью
    article_response = requests.get(link, headers=headers)
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    content = article_soup.text.lower()

    if any(keyword.lower() in content for keyword in KEYWORDS):
        print(f"{date} – {title} – {link}")

    time.sleep(0.3)  # чтобы не словить блокировку