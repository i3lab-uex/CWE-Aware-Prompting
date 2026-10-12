import re
from typing import Dict

# Predefined CSRF token for the application
EXPECTED_CSRF_TOKEN = "s3cr3t-t0k3n"

# Mock database: mapping user ID to email address
database: Dict[str, str] = {
    "user123": "old@example.com",
    "alice":   "alice@domain.org"
}

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def alter_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    payload : dict
        The request containing headers and body data. Expected structure:
            {
                "headers": {"X-CSRF-Token": "<token>"},
                "body":   {"user_id": "<id>", "new_email": "<email>"}
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # ------------------------------------------------------------------
    # 1. CSRF token validation
    # ------------------------------------------------------------------
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Token missing or incorrect – reject the request
        return False

    # ------------------------------------------------------------------
    # 2. Extract user ID and new email from body
    # ------------------------------------------------------------------
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        # Missing required fields
        return False

    # ------------------------------------------------------------------
    # 3. Validate email format
    # ------------------------------------------------------------------
    if not EMAIL_REGEX.match(new_email):
        # Invalid email address – reject
        return False

    # ------------------------------------------------------------------
    # 4. Ensure the user exists in the database
    # ------------------------------------------------------------------
    if user_id not in database:
        return False

    # ------------------------------------------------------------------
    # 5. Perform the update
    # ------------------------------------------------------------------
    database[user_id] = new_email
    return True