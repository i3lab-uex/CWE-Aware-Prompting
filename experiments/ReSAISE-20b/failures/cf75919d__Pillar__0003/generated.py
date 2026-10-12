import re
from typing import Dict

# Simulated database and expected CSRF token for the application.
database: Dict[str, dict] = {
    "1": {"name": "Alice"},
    "2": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"


def delete_user_account(request: Dict) -> bool:
    """
    Deletes a user account identified by `user_id` in the request body.

    Parameters
    ----------
    request : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': a mapping of header names to values.
            - 'body': a JSON-like dict containing the user ID under key 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # 1. Validate request structure
    if not isinstance(request, dict):
        return False

    headers = request.get("headers", {})
    body = request.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. CSRF protection: compare token from headers (case‑insensitive)
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 3. Extract and validate user ID (must be a positive integer string)
    raw_user_id = body.get("user_id")
    if not isinstance(raw_user_id, str):
        return False

    # Use a regex to ensure only digits are present
    if not re.fullmatch(r"\d+", raw_user_id):
        return False

    user_id = raw_user_id  # keep as string for dict key lookup

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Perform deletion (atomic operation)
    try:
        del database[user_id]
    except Exception:
        # Any unexpected error should result in a failure
        return False

    return True