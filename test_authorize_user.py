#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify whether stored DemoQA credentials are authorized via the API.

Author: Otávio Augusto
Date: 2025-10-19
Description:
    - Read the stored username and password from `.env`.
    - Submit the credentials to `/Account/v1/Authorized` to confirm access rights.
    - Print a human-readable message indicating whether authorization succeeded.
    - Surface HTTP errors and unexpected responses so the caller can react.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv


DEMOQA_AUTHORIZED_URL = "https://demoqa.com/Account/v1/Authorized"


def main() -> None:
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
            DEMOQA_AUTHORIZED_URL,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )
    except requests.RequestException as exc:
        print(f"HTTP request failed: {exc}")
        sys.exit(1)

    if response.status_code == 200:
        try:
            body = response.json()
        except json.JSONDecodeError:
            print("Response did not contain valid JSON data.")
            sys.exit(1)

        if body is True:
            print("User is authorized.")
        elif body is False:
            print("User is NOT authorized.")
        else:
            print(f"Unexpected response format: {body}")
            sys.exit(1)
    else:
        print(f"Failed to verify authorization (status {response.status_code}): {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()


