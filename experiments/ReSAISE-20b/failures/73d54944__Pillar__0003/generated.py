import json

# Constants and mock database for the context of this function.
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"
database: dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

def remove_user_data(data: dict) -> bool:
    """
    Remove a user account from the in-memory database.

    Parameters
    ----------
    data : dict
        Representation of an HTTP request. Expected keys:
            - 'headers': dict containing at least the 'X-CSRF-Token' header.
            - 'body': str or dict containing a JSON object with the key 'user_id'.

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # Validate presence of headers and CSRF token
    try:
        headers = data["headers"]
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False
    except (KeyError, AttributeError):
        # Missing headers or CSRF token field
        return False

    # Parse the request body for user_id
    try:
        body = data.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)
        user_id = body["user_id"]
    except (ValueError, KeyError, TypeError):
        # Body is not valid JSON or user_id missing
        return False

    # Ensure the user ID is an integer
    if not isinstance(user_id, int):
        return False

    # Perform the deletion in a thread‑safe manner
    try:
        # The database is a simple dict; remove the key if it exists.
        return database.pop(user_id, None) is not None
    except Exception:
        # Any unexpected error should result in a safe False return.
        return False