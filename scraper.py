import logging
import os
import random

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

NEWS_BASE = os.getenv("NEWS_BASE")
TOP_URL = os.getenv("TOP_URL")

USER_AGENT = os.getenv(
    "USER_AGENT",
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        + "AppleWebKit/537.36 (KHTML, like Gecko) "
        + "Chrome/122.0.0.0 Safari/537.36"
    ),
)


def get_random_news_article():
    """
    Fetches a random Japanese article URL.
    Returns the URL as a string."""
    articles = get_recent_news_articles()

    random.shuffle(articles)
    random_article = articles[0]

    news_id = random_article["news_id"]
    article_url = f"{NEWS_BASE}{news_id}/{news_id}.html"

    return article_url


def get_recent_news_articles():
    """
    Gets recent articles from the news website.
    Returns a list of article URLs.
    """
    url = TOP_URL
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching the article list: {e}")
        return None

    articles = response.json()
    if not articles:
        logger.error("No articles found.")
        return None

    return [
        f"{NEWS_BASE}{article['news_id']}/{article['news_id']}.html"
        for article in articles
    ]


def scrape_news_article(url):
    """
    Scrapes a Japanese article for its title and content.
    Returns a dictionary with 'title' and 'content'.
    """
    headers = {
        "User-Agent": USER_AGENT,
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching the article: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    # Find the content
    content_tag = soup.find("div", id="js-article-body")
    content = content_tag.get_text(strip=True) if content_tag else "No content found"

    return {"title": title, "content": content}
