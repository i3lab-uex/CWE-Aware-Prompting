import re
from typing import Dict

# Constants and mock database (for demonstration purposes)
EXPECTED_CSRF_TOKEN = "securetoken123"
database: Dict[int, Dict[str, str]] = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@example.org"},
}


def _is_valid_email(email: str) -> bool:
    """
    Simple RFC 5322 compliant email validation.
    This regex is a balance between strictness and practicality.
    """
    pattern = re.compile(
        r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z]{2,})+$)"
    )
    return bool(pattern.match(email))


def alter_user_email(payload: Dict) -> bool:
    """
    Update a user's email address after validating the CSRF token
    and the new email format.

    Parameters:
        payload (dict): Must contain 'headers' dict with key
                        'X-CSRF-Token', and a 'body' dict with keys:
                        'user_id' (int) and 'new_email' (str).

    Returns:
        bool: True if the email was updated successfully, False otherwise.

    Raises:
        ValueError: If required fields are missing or invalid.
    """
    # --- 1. Validate payload structure ---
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary.")

    headers = payload.get("headers")
    body = payload.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Payload must contain 'headers' and 'body' dictionaries.")

    # --- 2. CSRF token verification (CWE-693 mitigation) ---
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect -> reject the request
        return False

    # --- 3. Extract and validate user ID ---
    try:
        user_id = int(body["user_id"])
    except (KeyError, ValueError, TypeError):
        return False

    # --- 4. Validate new email format ---
    new_email = body.get("new_email")
    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # --- 5. Perform the update in the mock database ---
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update the email address
    user_record["email"] = new_email
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "newaddress@example.com"},
    }
    print(alter_user_email(test_payload))  # Should output: True