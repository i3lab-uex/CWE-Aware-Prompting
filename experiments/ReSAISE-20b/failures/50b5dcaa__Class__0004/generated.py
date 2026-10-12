import re
from typing import Dict

# Mock database and CSRF token (normally these would be defined elsewhere)
database: Dict[int, dict] = {
    1: {"email": "old@example.com", "name": "Alice"},
    2: {"email": "bob@example.org", "name": "Bob"},
}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$"
)


def edit_user_email(req_payload: dict) -> bool:
    """
    Update a user's email address after validating CSRF token and
    ensuring the provided data is authentic.

    Parameters:
        req_payload (dict): HTTP request payload containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":   {
                        "user_id": <int>,
                        "new_email": "<email>"
                    }
                }

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token mismatch; treat as failure
        return False

    # 2. Extract body data safely
    body = req_payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Validate presence of required fields
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Ensure user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update the email
    user_record["email"] = new_email
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    payload = {
        "headers": {"X-CSRF-Token": "secure_token_123"},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    result = edit_user_email(payload)
    print("Update succeeded:", result)  # Expected: True
    print("Updated record:", database[1])