import re
from typing import Dict

# Global context variables (would normally be provided by the framework)
database: Dict[int, Dict[str, str]] = {}
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF protection
    and basic input validation.

    Parameters
    ----------
    query : dict
        The request payload. Expected keys:
            - "headers": dict containing HTTP headers (e.g., "X-CSRF-Token")
            - "body": dict containing:
                * "user_id" (int or str convertible to int)
                * "new_email" (str)

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – potential CSRF or malformed request
        return False

    # 2. Extract and validate body parameters
    body = query.get("body", {})
    user_id_raw = body.get("user_id")
    new_email = body.get("new_email")

    # Validate presence
    if user_id_raw is None or new_email is None:
        return False

    # Convert user ID to int safely
    try:
        user_id = int(user_id_raw)
    except (ValueError, TypeError):
        return False

    # Validate email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Check if user exists in the mock database
    user_record = database.get(user_id)
    if not isinstance(user_record, dict):
        return False

    # 4. Perform the update
    user_record["email"] = new_email.strip()
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Seed mock database
    database[1] = {"email": "old@example.com", "name": "Alice"}

    # Correct request
    query_valid = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice@example.org"}
    }
    assert change_user_email(query_valid) is True
    assert database[1]["email"] == "alice@example.org"

    # Invalid CSRF token
    query_bad_csrf = {
        "headers": {"X-CSRF-Token": "bad-token"},
        "body": {"user_id": 1, "new_email": "alice@example.org"}
    }
    assert change_user_email(query_bad_csrf) is False

    # Invalid email format
    query_bad_email = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "invalid-email"}
    }
    assert change_user_email(query_bad_email) is False

    print("All tests passed.")