import re
from typing import Dict, Any

# Mock database and CSRF token (normally these would be defined elsewhere)
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def modify_user_email(req_data: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_data : dict
        HTTP request representation containing headers and body.
        Expected keys:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body': dict containing:
                - 'user_id': str or int
                - 'new_email': str

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Verify CSRF token authenticity
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid token – potential CSRF attack
        return False

    # 2. Retrieve and validate request body
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Basic type checks
    if user_id is None or new_email is None:
        return False

    # 3. Validate the new email format
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure the user exists in the database
    if str(user_id) not in database:
        return False

    # 5. Update the email address
    try:
        database[str(user_id)]["email"] = new_email
    except Exception:
        # Any unexpected error during the update results in failure
        return False

    return True


# ------------------------------------------------------------------
# Example usage (for illustration; remove or comment out in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Seed mock database
    database["42"] = {"email": "old@example.com", "name": "Alice"}

    # Construct a valid request
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42, "new_email": "alice@example.org"},
    }

    result = modify_user_email(request)
    print("Update successful:", result)  # Expected: True
    print("Updated record:", database["42"])