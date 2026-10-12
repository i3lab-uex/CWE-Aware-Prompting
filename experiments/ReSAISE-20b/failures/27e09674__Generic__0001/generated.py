import re

# Simulated in‑memory database and CSRF token constant
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.org"},
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def _is_valid_email(email: str) -> bool:
    """Simple regex check for email validity."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
    return re.match(pattern, email) is not None

def change_user_email(query: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {
                    "user_id": <int>,
                    "new_email": "<email>"
                }
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # Validate CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract body data
    body = query.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Basic validation
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # Validate email format
    if not _is_valid_email(new_email):
        return False

    # Check that user exists in the database
    if user_id not in database:
        return False

    # Update email
    database[user_id]["email"] = new_email
    return True