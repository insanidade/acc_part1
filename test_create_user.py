#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create and persist DemoQA Book Store API user credentials.

Generates secure credentials, invokes the Create User endpoint, and stores
identifiers for subsequent API calls.

Author: Otávio Augusto
Date: 2025-10-19
Description:
    - Generate a random username and password that satisfy DemoQA complexity rules.
    - Call the `/Account/v1/User` endpoint to create the account.
    - Persist the username, password, and returned user ID into the local `.env` file
      so downstream scripts can authenticate with the same credentials.
    - Provide clear console output for both successful and failed API interactions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
import secrets
import string


DEMOQA_CREATE_USER_URL = "https://demoqa.com/Account/v1/User"

ENV_FILE_PATH = Path(__file__).resolve().with_name(".env")

# Restrict the set of special characters to a safe subset that the API
# accepts consistently.
SPECIAL_CHARACTERS = "!@#$%&*"


def generate_secure_password(length: int = 12) -> str:
    """Return a random password that satisfies DemoQA's complexity rules.

    The password contains at least one uppercase, lowercase, digit, and
    special character. The remaining characters are drawn from a mix of all
    categories using the secrets module for cryptographic randomness.
    """

    if length < 8:
        raise ValueError("Password length must be at least 8 characters")

    alphabet = string.ascii_letters + string.digits + SPECIAL_CHARACTERS
    system_random = secrets.SystemRandom()

    password_chars = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(SPECIAL_CHARACTERS),
    ]

    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(alphabet))

    system_random.shuffle(password_chars)

    return "".join(password_chars)


def generate_unique_username(base: str = "testuser", suffix_length: int = 5) -> str:
    """Create a username by appending a random zero-padded numeric suffix."""

    max_value = 10 ** suffix_length
    suffix = str(secrets.randbelow(max_value)).zfill(suffix_length)
    return f"{base}{suffix}"


def create_user(user_name: str, password: str) -> tuple[int, dict[str, str]]:
    """Call the DemoQA Create User endpoint and return status code + payload."""

    payload = {"userName": user_name, "password": password}

    response = requests.post(
        DEMOQA_CREATE_USER_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=10,
    )

    try:
        data = response.json()
    except json.JSONDecodeError:
        data = {"message": response.text.strip() or "No response body returned"}

    return response.status_code, data


def load_env_values(env_path: Path) -> dict[str, str]:
    """Return existing key/value pairs from a .env file if present."""

    env_values: dict[str, str] = {}

    if not env_path.exists():
        return env_values

    with env_path.open("r", encoding="utf-8") as env_file:
        for line in env_file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            env_values[key.strip()] = value.strip()

    return env_values


def save_credentials_to_env(credentials: dict[str, str], env_path: Path = ENV_FILE_PATH) -> None:
    """Persist the provided credentials to the given .env file."""

    existing_values = load_env_values(env_path)
    existing_values.update(credentials)

    with env_path.open("w", encoding="utf-8") as env_file:
        for key, value in existing_values.items():
            env_file.write(f"{key}={value}\n")


def main() -> None:
    """Generate credentials, print them, and attempt to create the user."""

    user_name = generate_unique_username()
    password = generate_secure_password()

    print(f"Generated username: {user_name}")
    print(f"Generated password: {password}")

    try:
        status_code, payload = create_user(user_name, password)
    except requests.RequestException as exc:
        print(f"HTTP request failed: {exc}")
        sys.exit(1)

    if status_code == 201:
        user_id = payload.get("userID", "<missing userID>")
        username_from_api = payload.get("username", user_name)
        print("Successfully created user!")
        print(f"userID: {user_id}")
        print(f"username: {username_from_api}")

        save_credentials_to_env(
            {
                "DEMOQA_USERNAME": username_from_api,
                "DEMOQA_PASSWORD": password,
                "DEMOQA_USER_ID": user_id,
            }
        )
        print(f"Saved credentials to {ENV_FILE_PATH}")
    else:
        error_message = payload.get("message") or payload
        print(f"Failed to create user (status {status_code}): {error_message}")
        sys.exit(1)


if __name__ == "__main__":
    main()


