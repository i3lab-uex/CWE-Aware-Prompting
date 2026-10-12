import json

# Constants and mock database for demonstration purposes
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
database: dict[str, dict] = {
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"},
}


def remove_user_data(data: dict) -> bool:
    """
    Remove a user account from the in-memory database.

    Parameters
    ----------
    data : dict
        Representation of an HTTP request containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id'

    Returns
    -------
    bool
        True if the account was removed successfully, otherwise False.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    # Validate request structure
    if not isinstance(data, dict):
        raise ValueError("Request data must be a dictionary.")

    headers = data.get("headers")
    body = data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Headers and body must be dictionaries.")

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid or missing CSRF token.")

    # Extract user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        raise ValueError("User ID must be a string.")

    # Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False


# Example usage (for testing purposes)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user1"},
    }
    print("Before:", database)
    result = remove_user_data(request)
    print("Removed:", result)
    print("After:", database)