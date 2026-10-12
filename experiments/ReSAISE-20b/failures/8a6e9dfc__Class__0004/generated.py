import re
from typing import Dict

# Simulated database and CSRF token (for demonstration purposes)
database: Dict[int, dict] = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def edit_user_email(payload: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Args:
        payload: A dictionary representing the incoming request. It must contain
                 a 'headers' dict with an 'X-CSRF-Token' key and a 'body'
                 dict with 'user_id' (int) and 'new_email' (str).

    Returns:
        True if the email was successfully updated, False otherwise.
    """
    # 1. Validate CSRF token
    headers = payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract body parameters safely
    body = payload.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # Ensure user_id is an integer
    if not isinstance(user_id, int):
        return False

    # Ensure new_email is a string and matches the regex
    if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
        return False

    # 3. Check that the user exists in the database
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 4. Perform the update (in a real scenario, this would involve
    #    database transaction handling and error checking)
    try:
        user_record["email"] = new_email
        return True
    except Exception:
        # Any unexpected error should result in a failure
        return False

# Example usage (for testing purposes)
if __name__ == "__main__":
    test_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "alice.new@example.com"}
    }
    print(edit_user_email(test_payload))  # Expected: True
    print(database[1]["email"])           # Expected: alice.new@example.com