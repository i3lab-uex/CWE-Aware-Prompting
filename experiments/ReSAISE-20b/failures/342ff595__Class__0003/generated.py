import json

# Constants and mock database (to be provided by the surrounding system)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"
database: dict[int, dict] = {}


def remove_user_profile(request_data: dict) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        A dictionary representing an HTTP request. It must contain:
            - 'headers': a dict with at least the key 'X-CSRF-Token'
            - 'body': a JSON string or dict containing the key 'user_id'

    Returns
    -------
    bool
        True if the user was found and removed, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # Validate CSRF token to guard against cross‑site request forgery
    headers = request_data.get("headers")
    if not isinstance(headers, dict):
        raise ValueError("Missing or invalid headers")

    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – do not proceed
        return False

    # Extract user ID from the body
    body = request_data.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("Body is not valid JSON")

    if not isinstance(body, dict):
        raise ValueError("Missing or invalid body")

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        raise ValueError("User ID must be an integer")

    # Perform deletion in a thread‑safe manner (not shown here; assume single‑threaded)
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False