import csv
import re
import sys
import time
import logging
from random import shuffle

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger(__name__)


from anki_api import add_anki_card, get_anki_sentences
from filter import filter_sentences_by_new_words
from get_anki_card import get_anki_card
from scraper import get_recent_news_articles, scrape_news_article


ADD_TO_ANKI = "--add-to-anki" in sys.argv
WRITE_DECK_NAME = "Erryday deck II: Electric boogaloo"

READ_DECK_NAMES = [WRITE_DECK_NAME, "Erryday deck"]

# article_url = get_random_news_article()

article_urls = get_recent_news_articles()

shuffle(article_urls)

article_urls = article_urls[:5]
existing_sentences = set()
article_sentences = set()

for article_url in article_urls:
    article = scrape_news_article(article_url)
    sentences = re.split(r"[。！？]", article["content"])
    article_sentences.update([s.strip() for s in sentences if s.strip()])

for deck in READ_DECK_NAMES:
    existing_sentences.update(get_anki_sentences('"' + deck + '"'))

result = filter_sentences_by_new_words(article_sentences, existing_sentences)
shuffle(result)
logger.debug("Sentences with new words:")
logger.debug(result[:10])

anki_cards = [get_anki_card(s[0]) for s in result[:10]]
timestamp = int(time.time())
CSV_FILE = f"anki_cards_{timestamp}.csv"

with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sentence", "reading", "meaning"])
    for card in anki_cards:
        writer.writerow(
            [
                card["reply"]["sentence"],
                card["reply"]["reading"],
                card["reply"]["meaning"],
            ]
        )


if ADD_TO_ANKI:
    for card in anki_cards:
        add_anki_card(card, WRITE_DECK_NAME)

logger.info("Wrote to file: %s", CSV_FILE)
