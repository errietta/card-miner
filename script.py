import csv
import re
import sys
import time

from dotenv import load_dotenv
load_dotenv()

from anki_api import add_anki_card, get_anki_sentences
from filter import filter_sentences_by_new_words
from get_anki_card import get_anki_card
from scraper import get_random_news_article, scrape_news_article


ADD_TO_ANKI = "--add-to-anki" in sys.argv
WRITE_DECK_NAME = "Erryday deck II: Electric boogaloo"

READ_DECK_NAMES = [WRITE_DECK_NAME, "Erryday deck"]

article_url = get_random_news_article()
article = scrape_news_article(article_url)

article_sentences = re.split(r"[。！？]", article["content"])
article_sentences = [s.strip() for s in article_sentences if s.strip()]

existing_sentences = set()

for deck in READ_DECK_NAMES:
    existing_sentences.update(get_anki_sentences('"' + deck + '"'))

result = filter_sentences_by_new_words(article_sentences, existing_sentences)
print("Sentences with new words:")
print(result[:10])

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

print("Wrote to file:", CSV_FILE)
