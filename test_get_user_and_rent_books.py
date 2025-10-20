#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retrieve DemoQA user details using stored credentials.

Author: Otávio Augusto
Date: 2025-10-19
Description:
    - Load the DemoQA user ID and token from `.env`.
    - Issue a GET request to `/Account/v1/User/{userId}` to obtain account metadata.
    - Print the raw status code and response body for inspection.
    - Exit with a non-zero status code if the API call does not succeed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


ACCOUNT_USER_URL_TEMPLATE = "https://demoqa.com/Account/v1/User/{user_id}"


def _get_env_value(key: str) -> str:
    from os import getenv

    value = getenv(key)
    if not value:
        print(f"Missing required environment variable: {key}")
        sys.exit(1)
    return value


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    env_path = base_dir / ".env"

    if not env_path.exists():
        print(f"Missing environment file: {env_path}")
        sys.exit(1)

    load_dotenv(env_path)

    user_id = _get_env_value("DEMOQA_USER_ID")
    token = _get_env_value("DEMOQA_TOKEN")

    url = ACCOUNT_USER_URL_TEMPLATE.format(user_id=user_id)

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as exc:
        print(f"HTTP request failed: {exc}")
        sys.exit(1)

    print("Response status:", response.status_code)
    print("Response body:")
    print(response.text)

    if response.status_code != 200:
        sys.exit(1)


if __name__ == "__main__":
    main()


