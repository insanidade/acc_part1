#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add two random DemoQA books to the authenticated user's collection.

Author: Otávio Augusto
Date: 2025-10-19
Description:
    - Load the DemoQA user ID and token from `.env` and the ISBN catalog JSON.
    - Randomly select two distinct ISBNs for rental.
    - Call `/BookStore/v1/Books` with the user's ID and ISBN list to add to the collection.
    - Print the full API response and terminate with an error code if the call fails.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from random import sample

import requests
from dotenv import load_dotenv


BOOKSTORE_ADD_BOOK_URL = "https://demoqa.com/BookStore/v1/Books"


def _load_env_value(key: str, env_path: Path) -> str:
    from os import getenv

    value = getenv(key)
    if not value:
        print(f"Missing required environment variable: {key}")
        sys.exit(1)
    return value


def _load_books(json_path: Path) -> dict[str, str]:
    if not json_path.exists():
        print(f"Books file not found: {json_path}")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Failed to parse books file: {exc}")
        sys.exit(1)

    if not isinstance(data, dict) or not data:
        print("Books file must contain a non-empty ISBN-to-title mapping.")
        sys.exit(1)

    return data


def main() -> None:
    base_path = Path(__file__).resolve().parent
    env_path = base_path / ".env"
    books_path = base_path / "test_books.json"

    if not env_path.exists():
        print(f"Missing environment file: {env_path}")
        sys.exit(1)

    load_dotenv(env_path)

    user_id = _load_env_value("DEMOQA_USER_ID", env_path)
    token = _load_env_value("DEMOQA_TOKEN", env_path)

    books = _load_books(books_path)
    isbns = list(books.keys())

    if len(isbns) < 2:
        print("Books file must contain at least two ISBN entries to proceed.")
        sys.exit(1)

    selected_isbns = sample(isbns, 2)

    payload = {
        "userId": user_id,
        "collectionOfIsbns": [{"isbn": isbn} for isbn in selected_isbns],
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.post(
            BOOKSTORE_ADD_BOOK_URL,
            headers=headers,
            json=payload,
            timeout=10,
        )
    except requests.RequestException as exc:
        print(f"HTTP request failed: {exc}")
        sys.exit(1)

    print("Response status:", response.status_code)
    print("Response body:")
    print(response.text)

    if response.status_code not in {200, 201}:
        sys.exit(1)


if __name__ == "__main__":
    main()


