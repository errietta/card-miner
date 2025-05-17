"""
    get_anki_card.py
    This script retrieves an access token from Auth0 for the AnkiMaker API
"""
import os
import json

import requests

class AccessTokenError(Exception):
    """Custom exception for access token retrieval errors."""


def get_token():
    """
        Retrieves an access token from Auth0 for the AnkiMaker API.
    """
    url = "https://cardmaker-dev.uk.auth0.com/oauth/token"

    payload = json.dumps({
        "client_id": os.environ.get("AUTH0_CLIENT_ID"),
        "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
        "audience": "https://card.backend/",
        "grant_type": "client_credentials"
    })
    headers = {
        'content-type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload, timeout=60)
    response.raise_for_status()

    response = response.json()

    if "access_token" in response:
        return response["access_token"]

    raise AccessTokenError("Failed to get access token: " + str(response))

def get_anki_card(text):
    """
        ```
        {
            "prompt": "これは例文です。",
            "reply": {
                "reading": "これは 例文[れいぶん]です。",
                "sentence": "これは例文です。",
                "meaning": "This is an example sentence."
            }
        }
        ```
    """
    url = "https://ankimaker-backend-88a288e4b6bb.herokuapp.com/meaning"
    print("Getting Anki card for: ", text)

    payload = json.dumps({
        "text": text,
    })
    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ' + get_token(),
    }

    response = requests.post(url, headers=headers, data=payload, timeout=60)
    return response.json()
    