import json

# Constants and mock database for demonstration purposes
EXPECTED_CSRF_TOKEN = "secure_token_123"
database: dict[int, dict] = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

def remove_user_profile(request_data: dict) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        A representation of an HTTP request containing headers and body.
        Expected keys:
            - 'headers': dict, must contain a 'X-CSRF-Token' key.
            - 'body': str or dict, JSON payload containing the user ID under the key 'user_id'.

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or data is malformed.
    """
    # Verify request structure
    if not isinstance(request_data, dict):
        raise ValueError("Request data must be a dictionary.")

    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (str, dict)):
        raise ValueError("Malformed request: headers and body required.")

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token: treat as a security failure
        return False

    # Parse body (JSON string or dict)
    if isinstance(body, str):
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("Body is not valid JSON.")
    else:
        payload = body

    # Extract user_id
    user_id_raw = payload.get("user_id")
    if user_id_raw is None:
        raise ValueError("Missing 'user_id' in request payload.")

    # Ensure user_id is an integer to avoid injection or type confusion
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        raise ValueError("'user_id' must be an integer.")

    # Remove user from database if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False