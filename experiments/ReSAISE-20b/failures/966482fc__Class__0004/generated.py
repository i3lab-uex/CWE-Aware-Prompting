import re
from typing import Dict

# Mock database and CSRF token (these would normally be defined elsewhere)
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def modify_user_email(req: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    req : dict
        The request dictionary expected to contain:
            - headers: dict with 'X-CSRF-Token' key
            - body: dict with 'user_id' and 'new_email' keys

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate input
    body = req.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Check that user exists in the mock database
    if user_id not in database:
        return False

    # 4. Update the user's email
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Log exception in real-world scenario
        return False

# Example usage (would normally be part of unit tests or application logic)
if __name__ == "__main__":
    # Setup a sample user
    database["user123"] = {"email": "old@example.com", "name": "Alice"}

    # Construct a request
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_email": "alice@example.com"}
    }

    success = modify_user_email(request)
    print("Update successful:", success)  # Should print True
    print("New email:", database["user123"]["email"])