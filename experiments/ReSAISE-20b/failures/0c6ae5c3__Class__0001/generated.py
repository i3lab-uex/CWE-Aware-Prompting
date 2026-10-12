#!/usr/bin/env python3
"""
Utility to delete a user account from an in‑memory database.

This module demonstrates a simple CSRF check and safe deletion
of a user entry. It is intentionally minimal, but includes
defensive programming to mitigate common weaknesses such as
CWE‑345 (Insufficient Verification of Data Authenticity).
"""

from __future__ import annotations

import logging
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration & Logging
# --------------------------------------------------------------------------- #

# The CSRF token expected by the server. In a real application this would
# be generated per session and stored securely.
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"

# Set up a basic logger. In production you would configure this more
# extensively (e.g., file handlers, rotation, etc.).
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(module)s] %(message)s",
)

# --------------------------------------------------------------------------- #
# Core Functionality
# --------------------------------------------------------------------------- #

def erase_user_account(
    request_info: Dict[str, Any],
    database: Dict[int, Dict[str, Any]],
) -> bool:
    """
    Delete a user account from the provided in‑memory database.

    Parameters
    ----------
    request_info : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': dict, should contain a 'X-CSRF-Token' key.
            - 'body': dict, must include an integer 'user_id'.
    database : dict
        The in‑memory user database. Keys are user IDs (int) and values
        are arbitrary dicts containing user data.

    Returns
    -------
    bool
        ``True`` if the account was successfully deleted,
        ``False`` otherwise (e.g., CSRF failure, missing user).

    Raises
    ------
    ValueError
        If the request format is invalid (missing keys, wrong types).
    """
    # ------------------------------------------------------------------- #
    # 1. Validate request structure
    # ------------------------------------------------------------------- #
    if not isinstance(request_info, dict):
        raise ValueError("request_info must be a dictionary")

    headers = request_info.get("headers")
    body = request_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("request_info must contain 'headers' and 'body' dictionaries")

    # ------------------------------------------------------------------- #
    # 2. Verify CSRF token
    # ------------------------------------------------------------------- #
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        logging.warning("CSRF token missing or not a string")
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        logging.warning("Invalid CSRF token: %s", csrf_token)
        return False

    # ------------------------------------------------------------------- #
    # 3. Extract user ID
    # ------------------------------------------------------------------- #
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        logging.warning("Missing 'user_id' in request body")
        return False

    # Accept either int or numeric string to be flexible
    if isinstance(user_id_raw, int):
        user_id = user_id_raw
    elif isinstance(user_id_raw, str) and user_id_raw.isdigit():
        user_id = int(user_id_raw)
    else:
        logging.warning("Invalid 'user_id' type: %r", user_id_raw)
        return False

    # ------------------------------------------------------------------- #
    # 4. Delete the user entry if it exists
    # ------------------------------------------------------------------- #
    if user_id in database:
        del database[user_id]
        logging.info("Deleted user account with ID %d", user_id)
        return True
    else:
        logging.warning("User ID %d not found in database", user_id)
        return False

# --------------------------------------------------------------------------- #
# Example usage (would normally be part of a test or application logic)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample in-memory database
    db = {
        1: {"name": "Alice"},
        2: {"name": "Bob"},
    }

    # Sample request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1}
    }

    success = erase_user_account(req, db)
    print(f"Deletion successful: {success}")
    print("Remaining database:", db)