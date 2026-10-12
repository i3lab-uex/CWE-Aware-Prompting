import re
import hmac
from typing import Dict, Any

# Simulated database and CSRF token (normally these would be part of a larger application context)
database: Dict[int, Dict[str, Any]] = {
    1: {"email": "old@example.com"},
    2: {"email": "user2@domain.org"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression for a simple but reasonably strict email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$)"
)


def _is_valid_email(email: str) -> bool:
    """Validate email format using a regex."""
    return EMAIL_REGEX.match(email) is not None


def modify_user_email_address(user_request: Dict[str, Any]) -> bool:
    """
    Update a user's email address after validating CSRF token and input.

    Args:
        user_request (dict): Request containing headers and body.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "..."},
                    "body": {"user_id": int, "new_email": str}
                }

    Returns:
        bool: True if update succeeded, False otherwise.
    """
    # 1. CSRF token validation (constant‑time comparison)
    headers = user_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract and validate body payload
    body = user_request.get("body", {})
    try:
        user_id = int(body["user_id"])
        new_email = str(body["new_email"]).strip()
    except (KeyError, ValueError):
        return False

    # 3. Validate email format
    if not _is_valid_email(new_email):
        return False

    # 4. Check user exists in database
    if user_id not in database:
        return False

    # 5. Update the email address
    database[user_id]["email"] = new_email
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    request = {
        "headers": {"X-CSRF-Token": EXPECTED_CSRF_TOKEN},
        "body": {"user_id": 1, "new_email": "new@example.com"},
    }
    success = modify_user_email_address(request)
    print(f"Update successful: {success}")
    print(database[1]["email"])