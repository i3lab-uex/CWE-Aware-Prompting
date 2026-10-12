import re
from typing import Dict, Any

# Mock database and CSRF token for demonstration purposes
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "old@example.com", "name": "Alice"},
    2: {"email": "bob@domain.org", "name": "Bob"}
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def modify_user_email(req_data: Dict[str, Any]) -> bool:
    """
    Update a user's email address after validating CSRF token and input data.

    Args:
        req_data: Dictionary containing HTTP request data, expected to have
                  'headers' and 'body'.  The body must contain:
                    - 'user_id': int
                    - 'new_email': str
                  The headers must contain:
                    - 'X-CSRF-Token': str

    Returns:
        bool: True if the email was updated successfully, False otherwise.

    Security considerations:
        - Validates CSRF token to mitigate protection mechanism failure (CWE-693).
        - Performs basic email format validation.
        - Checks that the user exists before updating.
    """
    # 1. CSRF protection: ensure token is present and matches expected value
    headers = req_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or invalid – reject the request
        return False

    # 2. Extract required fields from body
    body = req_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic validation of input types
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check that the user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the email address
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # In a real application, log the exception details securely
        return False