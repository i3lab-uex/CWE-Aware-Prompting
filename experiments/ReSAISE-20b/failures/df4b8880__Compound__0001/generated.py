import re

# Global context for the function (normally provided by the application)
database = {}
EXPECTED_CSRF_TOKEN = "s3cr3t-csrf-token"

# Regular expression for a basic email validation
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([^"\r\\]|\\["\r\\])*")@'
    r'([A-Z0-9]([-A-Z0-9]*[A-Z0-9])?\.)+[A-Z]{2,}$',
    re.IGNORECASE
)


def alter_user_email(payload: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Args:
        payload (dict): Request containing 'headers' and 'body'.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":   {"user_id": <id>, "new_email": "<email>"}
                }

    Returns:
        bool: True if the update succeeded, False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = payload.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # Token missing or incorrect
            return False

        # 2. Extract body data
        body = payload.get("body", {})
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        # 3. Basic input validation
        if user_id is None or new_email is None:
            return False

        # Ensure email has a valid format
        if not isinstance(new_email, str) or not EMAIL_REGEX.match(new_email):
            return False

        # 4. Update the database
        if user_id not in database:
            return False

        # Store only the sanitized email (lowercased for consistency)
        database[user_id]["email"] = new_email.lower()
        return True

    except Exception:
        # Any unexpected error results in failure
        return False


# Example usage (for demonstration only; remove or adapt for real tests)
if __name__ == "__main__":
    # Seed the mock database
    database[42] = {"email": "old@example.com", "name": "Alice"}

    # Successful update
    payload_success = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 42, "new_email": "new@example.com"}
    }
    print(alter_user_email(payload_success))  # True
    print(database[42]["email"])              # new@example.com

    # Failure due to wrong CSRF token
    payload_fail = {
        "headers": {"X-CSRF-Token": "invalid"},
        "body": {"user_id": 42, "new_email": "hack@example.com"}
    }
    print(alter_user_email(payload_fail))     # False