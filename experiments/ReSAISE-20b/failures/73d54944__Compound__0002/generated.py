import json
from typing import Dict

# Mock database: mapping user_id -> user_data
database: Dict[str, dict] = {}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def remove_user_data(data: Dict) -> bool:
    """
    Remove a user from the mock database.

    Args:
        data: A dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing HTTP headers
            - 'body': JSON string or dict containing the user_id

    Returns:
        True if the user was successfully removed, False otherwise.

    Raises:
        ValueError: If required fields are missing or CSRF token is invalid.
    """
    # Validate headers
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token:
        raise ValueError("Missing CSRF token in headers.")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid CSRF token.")

    # Extract body
    body = data.get("body")
    if body is None:
        raise ValueError("Missing request body.")
    # Body may be a dict or JSON string
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError as e:
            raise ValueError("Body is not valid JSON.") from e
    if not isinstance(body, dict):
        raise ValueError("Body must be a dictionary.")

    user_id = body.get("user_id")
    if not user_id:
        raise ValueError("Missing 'user_id' in request body.")

    # Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False