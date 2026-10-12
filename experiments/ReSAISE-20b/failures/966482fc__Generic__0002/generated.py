import re
from typing import Dict

# Simulated database and CSRF token (would normally be defined elsewhere)
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)


def modify_user_email(req: Dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing at least the CSRF token under
              'X-CSRF-Token'.
            - 'body': dict containing:
                - 'user_id' (int or str that can be converted to int)
                - 'new_email' (str)

    Returns
    -------
    bool
        True if the email was successfully updated, False otherwise.
    """
    # Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract body data
    body = req.get("body", {})
    user_id_raw = body.get("user_id")
    new_email = body.get("new_email")

    if user_id_raw is None or new_email is None:
        return False

    # Convert user ID to integer
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # Validate email format
    if not EMAIL_REGEX.match(new_email):
        return False

    # Ensure user exists in the database
    if user_id not in database:
        return False

    # Update the email address
    try:
        database[user_id]["email"] = new_email
        return True
    except Exception:
        # Catch any unexpected errors during the update
        return False


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    # Populate mock database
    database[1] = {"email": "old@example.com"}

    request_payload = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "new@example.com"},
    }

    success = modify_user_email(request_payload)
    print("Update successful:", success)  # Should print: Update successful: True