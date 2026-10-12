import json

# Simulated database and CSRF token for the example
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "securetoken123"

def discard_user(req_info: dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    req_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": mapping of header names to values.
              Must contain the key "X-CSRF-Token" with a matching token.
            - "body": JSON string containing the field "user_id".

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.

    Raises
    ------
    ValueError
        If the request format is invalid or required fields are missing.
    """
    # 1. Validate presence of headers and body
    if not isinstance(req_info, dict):
        raise ValueError("Request information must be a dictionary.")

    headers = req_info.get("headers")
    body = req_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, str):
        raise ValueError("Headers must be a dict and body a JSON string.")

    # 2. Verify CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # Token mismatch – reject silently

    # 3. Parse body safely
    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False  # Malformed JSON

    user_id = payload.get("user_id")
    if not isinstance(user_id, int):
        return False  # Invalid or missing user ID

    # 4. Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False