import re

# Example context variables (would normally be provided by the surrounding application)
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.com"}
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def change_user_email(query: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        Request data containing:
            - headers: dict with 'X-CSRF-Token'
            - body: dict with 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    - The function performs basic CSRF token validation.
    - It checks that the user exists and that the new email is in a valid format.
    """
    try:
        headers = query.get("headers", {})
        body = query.get("body", {})

        # CSRF protection
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract user id and new email
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if user_id is None or new_email is None:
            return False

        # Validate email format
        if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
            return False

        # Ensure user exists in the mock database
        if user_id not in database:
            return False

        # Perform the update
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # In production code we would log the exception
        return False