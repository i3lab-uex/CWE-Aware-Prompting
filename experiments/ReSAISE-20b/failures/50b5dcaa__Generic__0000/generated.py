import re
from typing import Dict, Any

# Mock database: user_id -> user dict
database: Dict[str, Dict[str, Any]] = {
    "1": {"email": "alice@example.com"},
    "2": {"email": "bob@example.org"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"


def _is_valid_email(email: str) -> bool:
    """
    Basic regex check for email validity.
    Not exhaustive but sufficient for demo purposes.
    """
    pattern = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$",
        re.IGNORECASE,
    )
    return bool(pattern.match(email))


def edit_user_email(req_payload: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req_payload : dict
        HTTP request representation containing:
            - headers: dict, may include 'X-CSRF-Token'
            - body: dict, must contain:
                * user_id : str
                * new_email : str

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # Validate CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract body data
    body = req_payload.get("body", {})
    user_id = str(body.get("user_id"))
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # Validate email format
    if not _is_valid_email(new_email):
        return False

    # Check user exists in database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # Update email
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # Any unforeseen error leads to failure
        return False