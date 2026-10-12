import re
from typing import Dict

# Simulated database: user_id -> dict with 'email' key
database: Dict[str, Dict[str, str]] = {}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN: str = "secure_expected_token_123"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9]([-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$)"
)


def change_user_email(new_request: Dict) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    new_request : dict
        The incoming request object containing headers and the body.
        Expected structure:
            {
                "headers": {"X-CSRF-Token": "..."},
                "body": {"user_id": "...", "new_email": "..."}
            }

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    try:
        # 1. Verify CSRF token (CWE-345 mitigation)
        headers = new_request.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # 2. Extract user_id and new_email
        body = new_request.get("body", {})
        user_id = str(body.get("user_id"))
        new_email = body.get("new_email", "").strip()

        # 3. Validate email format
        if not EMAIL_REGEX.match(new_email):
            return False

        # 4. Ensure user exists in the database
        if user_id not in database:
            return False

        # 5. Update the email
        database[user_id]["email"] = new_email
        return True

    except Exception:
        # Any unexpected error should result in a safe failure
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Setup a sample user
    database["user123"] = {"email": "old@example.com"}

    # Prepare a request
    req = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": "user123", "new_email": "new@example.com"}
    }

    result = change_user_email(req)
    print("Update successful:", result)
    print("Updated email:", database["user123"]["email"])