import re
from typing import Dict

# Mock database and CSRF token for demonstration purposes
database: Dict[str, Dict] = {
    "1": {"email": "old@example.com", "name": "Alice"},
    "2": {"email": "bob@example.org", "name": "Bob"},
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def change_user_email(request_data: Dict) -> bool:
    """
    Update the email address of a user.

    Parameters
    ----------
    request_data : dict
        Dictionary representing the HTTP request. Expected keys:
            - headers: dict containing at least 'X-CSRF-Token'
            - body: dict with keys 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # 1. CSRF protection: ensure token is present and matches expected value
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id and new_email from the request body
    body = request_data.get("body", {})
    user_id = str(body.get("user_id"))  # cast to string for key lookup
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate the new email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Ensure the user exists in the mock database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the user's email safely
    try:
        # In a real application, additional checks (e.g., uniqueness) would be needed
        user_record["email"] = new_email
    except Exception:
        # Any unexpected error results in a failure
        return False

    return True