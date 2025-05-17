import re

from dotenv import load_dotenv

load_dotenv()

from anki_api import get_anki_sentences
from filter import filter_sentences_by_new_words
from scraper import get_random_news_article, scrape_news_article



article_url = get_random_news_article()
article = scrape_news_article(article_url) 


article_sentences = re.split(r'[。！？]', article['content'])
article_sentences = [s.strip() for s in article_sentences if s.strip()]


existing_sentences = set(get_anki_sentences('"Erryday deck II: Electric boogaloo"'))
existing_sentences.update(get_anki_sentences('"Erryday deck"'))


result = filter_sentences_by_new_words(article_sentences, existing_sentences)
print("Sentences with new words:")
for s in result:
    print("-", s)
