import re
from typing import Dict

# Mock database: user_id -> {"email": str, ...}
database: Dict[str, dict] = {}

# CSRF token expected in request headers
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Simple email validation regex (RFC 5322 compliant is complex; this covers common cases)
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([^\"]|\\")*"'
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}$',
    re.IGNORECASE
)


def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address after validating CSRF token and request body.

    Parameters
    ----------
    request_data : dict
        Dictionary containing at least the following keys:
            - 'headers': dict with HTTP headers, e.g. {'X-CSRF-Token': '...'}
            - 'body': dict with request body, e.g. {'user_id': '123', 'new_email': 'foo@example.com'}

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id and new_email from body
    body = request_data.get("body", {})
    user_id = str(body.get("user_id") or body.get("id")).strip()
    new_email = str(body.get("new_email") or body.get("email", "")).strip()

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real application, log the exception
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate mock database
    database["1"] = {"email": "old@example.com", "name": "Alice"}

    # Prepare a request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "1", "new_email": "alice@example.com"},
    }

    success = change_user_email(req)
    print("Update succeeded:", success)
    print("Updated record:", database["1"])