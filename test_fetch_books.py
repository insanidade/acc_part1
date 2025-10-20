#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch DemoQA books and store an ISBN-to-title map as JSON.

Author: Otávio Augusto
Date: 2025-10-19
Description:
    - Query `/BookStore/v1/Books` to retrieve the catalog of books.
    - Extract each book's ISBN and title, ignoring malformed entries.
    - Save the resulting mapping to `test_books.json` for later API calls.
    - Handle HTTP and parsing errors gracefully with descriptive messages.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests


BOOKS_ENDPOINT = "https://demoqa.com/BookStore/v1/Books"
OUTPUT_FILE = Path(__file__).resolve().with_name("test_books.json")


def main() -> None:
    try:
        response = requests.get(
            BOOKS_ENDPOINT,
            headers={"Accept": "application/json"},
            timeout=10,
        )
    except requests.RequestException as exc:
        print(f"HTTP request failed: {exc}")
        sys.exit(1)

    if response.status_code != 200:
        print(f"Failed to fetch books (status {response.status_code}): {response.text}")
        sys.exit(1)

    try:
        payload = response.json()
    except json.JSONDecodeError:
        print("Response did not contain valid JSON data.")
        sys.exit(1)

    books = payload.get("books")
    if not isinstance(books, list):
        print("Unexpected response format: 'books' list missing.")
        sys.exit(1)

    isbn_to_title: dict[str, str] = {}
    pretty_details: list[str] = []

    for book in books:
        if not isinstance(book, dict):
            continue
        isbn = book.get("isbn")
        title = book.get("title")
        authors = book.get("author")

        if isinstance(isbn, str) and isinstance(title, str):
            isbn_to_title[isbn] = title

            if isinstance(authors, str) and authors.strip():
                author_str = authors.strip()
            else:
                author_str = "<no author provided>"

            pretty_details.append(
                f"ISBN: {isbn}\nTitle: {title}\nAuthors: {author_str}\n"
            )

    if not isbn_to_title:
        print("No books with valid ISBN and title entries found.")
        sys.exit(1)

    print("Fetched book details:")
    print("\n".join(pretty_details))

    OUTPUT_FILE.write_text(
        json.dumps(isbn_to_title, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"Saved {len(isbn_to_title)} books to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()


