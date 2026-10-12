from __future__ import annotations

import re
from typing import Dict, Any

# Mock database and CSRF token (would normally be stored securely)
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "phone": "555-0100"},
    2: {"name": "Bob",   "phone": "555-0200"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression to validate a simple phone number format
PHONE_RE = re.compile(r"^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")


def alter_user_phone(incoming_request: Dict[str, Any]) -> bool:
    """
    Update a user's phone number in the mock database.

    Parameters
    ----------
    incoming_request : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': a mapping of header names to values
            - 'body':   a mapping containing 'user_id' (int) and 'new_phone' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * CSRF protection: The request must contain the expected token in the
      'X-CSRF-Token' header.
    * Input validation: The user ID must exist in the database and the
      phone number must match a simple pattern.
    * The function mutates the global `database` dictionary in place.
    """
    # 1. Validate headers and CSRF token
    try:
        headers = incoming_request["headers"]
        csrf_token = headers.get("X-CSRF-Token", "")
    except (KeyError, AttributeError):
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    try:
        body = incoming_request["body"]
        user_id = int(body.get("user_id"))
        new_phone: str = body.get("new_phone", "")
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Validate phone number format
    if not PHONE_RE.match(new_phone):
        return False

    # 4. Update the database
    if user_id not in database:
        return False

    # Simulate a transactional update
    try:
        database[user_id]["phone"] = new_phone
    except Exception:
        return False

    return True