# card-miner

## Description

This is for educational use only.
The script will scrape a news website for new vocabulary that doesn't already exist in your Anki Deck.
It will then use https://github.com/errietta/ankimaker-backend/tree/main to create new anki cards (right now in csv format) for those sentences.

As with any scraper, care must be taken to not abuse the service.

## Install

`pip install -r requirements.txt`

Use:

Set the following environment variables (or use `.env` file):

```
NEWS_BASE=
TOP_URL=
AUTH0_CLIENT_ID=
AUTH0_CLIENT_SECRET=
```

See `script.py` for an example script.
The script will generate a file in the format of `anki_cards_1747514472.csv`

You can also use `python script.py  --add-to-anki` to add to the deck automatically
(Not my fault if you destroy your deck.)

## TODO
Caching could also be implemented for both the Anki list and the website scraping.