import re
from typing import Dict

# Pre‑defined CSRF token (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

# Mock database – key is user id, value is a dict with at least an 'email' field
database: Dict[str, Dict] = {
    "user1": {"email": "old@example.com"},
    "user2": {"email": "another@domain.com"},
}

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    query : dict
        Expected keys:
            - headers: dict containing 'X-CSRF-Token'
            - body: dict containing 'user_id' and 'new_email'

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = query.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract body data
    body = query.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not user_id or not new_email:
        return False

    # 3. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 4. Check that the user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 5. Update the email
    try:
        user_record["email"] = new_email
    except Exception:
        return False

    return True