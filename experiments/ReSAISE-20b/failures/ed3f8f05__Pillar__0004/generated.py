import re
from typing import Dict

# Mock database and CSRF token (for demonstration purposes)
database: Dict[int, dict] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def change_user_email(request_data: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    request_data : dict
        Expected to contain:
            - 'headers': dict with at least a 'X-CSRF-Token' key.
            - 'body': dict with keys:
                * 'user_id': int
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """

    # 1. CSRF token validation (CWE-693 mitigation)
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate body data
    body = request_data.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, int) or user_id <= 0:
        return False
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Check that the user exists
    if user_id not in database:
        return False

    # 4. Update the email
    try:
        database[user_id]["email"] = new_email.strip()
    except Exception:
        # Any unexpected error during update results in failure
        return False

    return True