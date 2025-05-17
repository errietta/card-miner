import os

import requests
from strip_tags import strip_tags

ANKI_SERVER = os.getenv("ANKI_SERVER", "http://192.168.1.125:8766")

def get_anki_sentences(deck_name=None):
    """
    Fetches sentences from Anki via AnkiConnect API.
    Optionally filters by deck name.
    Returns a list of sentences (strings).
    """
    # Find note IDs in deck
    query = {"action": "findNotes", "version": 6, "params": {}}
    if deck_name:
        query["params"]["query"] = f"deck:{deck_name}"
    else:
        query["params"]["query"] = ""


    response = requests.post(ANKI_SERVER, json=query, timeout=60)
    note_ids = response.json().get("result", [])
    if not note_ids:
        print(f"No notes found in deck '{deck_name}'")
        return []

    print(f"Found {len(note_ids)} notes in deck '{deck_name}'")
    # Fetch note info
    notes_query = {"action": "notesInfo", "version": 6, "params": {"notes": note_ids}}

    notes_response = requests.post(ANKI_SERVER, json=notes_query, timeout=60)
    notes = notes_response.json().get("result", [])
    # Extract sentences (assume field named 'Sentence' or use first field)

    sentences = []
    for note in notes:
        fields = note.get("fields", {})
        if "Sentence" in fields:
            value = fields["Sentence"]["value"]
            value = strip_tags(value)
            sentences.append(value)
        elif fields:
            first_field = next(iter(fields.values()))
            value = first_field["value"]
            value = strip_tags(value)
            sentences.append(value)
    return sentences

def add_anki_card(card, deck_name):
    """
    Adds a card to the specified Anki deck using the AnkiConnect API.

    Args:
        card (dict): A dictionary containing card information. Expected to have a 'reply' key with subkeys:
            - 'sentence' (str): The expression or front of the card.
            - 'meaning' (str): The meaning or back of the card.
            - 'reading' (str): The reading or pronunciation of the card.
        deck_name (str): The name of the Anki deck to add the card to.

    Sends a POST request to the AnkiConnect server to add the card. Prints a success message if the card is added,
    otherwise prints a failure message.
    """
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Tango Card Format",
                "fields": {
                    "Expression": card["reply"]["sentence"],
                    "Meaning": card["reply"]["meaning"],
                    "Reading": card["reply"]["reading"],
                },
                "options": {"allowDuplicate": False},
                "tags": ["auto-added"],
            }
        },
    }
    response = requests.post(ANKI_SERVER, json=payload, timeout=60)
    if response.ok:
        print(f"Added to Anki: {card['reply']['sentence']}")
    else:
        print(f"Failed to add: {card['reply']['sentence']}")
