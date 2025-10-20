#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate and persist a DemoQA Book Store API authentication token.

Author: Otávio Augusto
Date: 2025-10-19
Description:
    - Load the stored username and password from `.env`.
    - Invoke the `/Account/v1/GenerateToken` endpoint using `requests`.
    - Persist the returned token back into `.env` via `python-dotenv`'s `set_key`.
    - Emit informative messages for both success and failure paths.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key


DEMOQA_GENERATE_TOKEN_URL = "https://demoqa.com/Account/v1/GenerateToken"


def main() -> None:
    """Load credentials, request a token, and persist it to .env."""

    env_path = Path(__file__).resolve().with_name(".env")

    if not env_path.exists():
        print(f"Missing environment file: {env_path}")
        sys.exit(1)

    load_dotenv(env_path)

    from os import getenv

    username = getenv("DEMOQA_USERNAME")
    password = getenv("DEMOQA_PASSWORD")

    if not username or not password:
        print("DEMOQA_USERNAME and DEMOQA_PASSWORD must be set in the .env file.")
        sys.exit(1)

    payload = {"userName": username, "password": password}

    try:
        response = requests.post(
            DEMOQA_GENERATE_TOKEN_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )
    except requests.RequestException as exc:
        print(f"HTTP request failed: {exc}")
        sys.exit(1)

    if response.status_code == 200:
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Response did not contain valid JSON data.")
            sys.exit(1)

        token = data.get("token")
        if not token:
            print("Token not found in the response payload.")
            sys.exit(1)

        set_key(str(env_path), "DEMOQA_TOKEN", token)
        print("Successfully retrieved and saved token.")
    else:
        print(f"Failed to generate token (status {response.status_code}): {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()


