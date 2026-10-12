import re
from typing import Dict

# Simulated database and CSRF token (would normally be global constants)
database: Dict[str, dict] = {
    "1": {"email": "old@example.com"},
    "2": {"email": "user2@domain.com"}
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def _is_valid_email(email: str) -> bool:
    """Return True if email matches the basic pattern."""
    return bool(EMAIL_REGEX.match(email))


def modify_user_email_address(user_request: dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    user_request : dict
        Incoming request object containing:
            - 'headers': dict with HTTP headers (must include 'X-CSRF-Token')
            - 'body'   : dict with keys 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    None
    """
    # 1. Verify CSRF token (authenticity check)
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – treat as potential forgery
        return False

    # 2. Extract request body and validate presence of required fields
    body = user_request.get("body", {})
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format to avoid injection or malformed data
    if not _is_valid_email(new_email):
        return False

    # 4. Ensure the user exists in the database (data authenticity)
    if str(user_id) not in database:
        return False

    # 5. Perform the update
    try:
        database[str(user_id)]["email"] = new_email
        return True
    except Exception:
        # Any unexpected failure results in a safe False
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_email": "new.email@example.com"}
    }
    print(modify_user_email_address(request))  # Expected: True
    print(database["1"]["email"])              # Expected: new.email@example.com