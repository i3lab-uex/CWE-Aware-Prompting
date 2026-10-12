import re
import hmac

# Mock database and CSRF token for demonstration purposes
database = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.com"}
}
EXPECTED_CSRF_TOKEN = "s3cr3t-t0k3n"

# Regular expression for a simple but reasonably strict email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+$)"
)


def _is_valid_email(email: str) -> bool:
    """Return True if email matches the expected pattern."""
    return EMAIL_REGEX.match(email) is not None


def change_user_email(query: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        The request payload containing:
            - 'headers': dict with at least a 'X-CSRF-Token' key.
            - 'body': dict containing 'user_id' (int) and 'new_email' (str).

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user ID and new email
    body = query.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = body["new_email"]
    except (KeyError, ValueError):
        return False

    # 3. Validate email format
    if not isinstance(new_email, str) or not _is_valid_email(new_email):
        return False

    # 4. Check that the user exists
    if user_id not in database:
        return False

    # 5. Perform the update
    database[user_id]["email"] = new_email
    return True