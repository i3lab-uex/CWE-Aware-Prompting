import re
from typing import Dict, Any

# Predefined CSRF token used for protection
EXPECTED_CSRF_TOKEN: str = "s3cr3t-csrf-token"

# Mock database simulating user data storage
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "user1@example.com"},
    2: {"email": "user2@example.com"},
}


def _is_valid_email(email: str) -> bool:
    """Simple regex to validate email format."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def change_user_email(query: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        Request containing headers and body data. Expected keys:
            - "headers": dict with "X-CSRF-Token" for CSRF protection
            - "body": dict containing:
                * "user_id": int or str convertible to int
                * "new_email": str

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = query.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract and validate user ID
        body = query.get("body", {})
        raw_user_id = body.get("user_id")
        if raw_user_id is None:
            return False
        try:
            user_id = int(raw_user_id)
        except (ValueError, TypeError):
            return False

        # 3. Validate new email format
        new_email = body.get("new_email")
        if not isinstance(new_email, str) or not _is_valid_email(new_email):
            return False

        # 4. Check if user exists in the database
        if user_id not in database:
            return False

        # 5. Update the email
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # In production code, log the exception here.
        return False