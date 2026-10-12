import re
from typing import Dict, Any

# Mock database and CSRF token (would normally be defined elsewhere)
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "old@example.com", "name": "Alice"},
    2: {"email": "bob@example.org", "name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def is_valid_email(email: str) -> bool:
    """Check if the provided string is a syntactically valid email address."""
    return isinstance(email, str) and EMAIL_REGEX.match(email) is not None


def modify_user_email(req_data: Dict[str, Any]) -> bool:
    """
    Update a user's email address.

    Parameters
    ----------
    req_data : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': mapping of header names to values
            - 'body':   mapping containing at least 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract body data
    body = req_data.get("body", {})
    try:
        user_id_raw = body["user_id"]
        new_email_raw = body["new_email"]
    except KeyError:
        # Required fields missing
        return False

    # 3. Validate and sanitize input
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    new_email = str(new_email_raw).strip()
    if not is_valid_email(new_email):
        return False

    # 4. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    user_record["email"] = new_email
    return True


# Example usage (for demonstration purposes only):
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"},
    }
    success = modify_user_email(request)
    print(f"Update successful: {success}")
    print(database[1]["email"])