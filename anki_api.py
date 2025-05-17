import requests
from strip_tags import strip_tags


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


    response = requests.post("http://192.168.1.125:8766", json=query, timeout=60)
    note_ids = response.json().get("result", [])
    if not note_ids:
        print(f"No notes found in deck '{deck_name}'")
        return []

    print(f"Found {len(note_ids)} notes in deck '{deck_name}'")
    # Fetch note info
    notes_query = {"action": "notesInfo", "version": 6, "params": {"notes": note_ids}}

    notes_response = requests.post("http://192.168.1.125:8766", json=notes_query, timeout=60)
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
