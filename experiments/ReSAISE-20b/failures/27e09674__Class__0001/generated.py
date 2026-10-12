import json
import re
from typing import Dict

# Simulated database: user_id -> dict with at least an "email" field
database: Dict[str, Dict] = {}

# Predefined CSRF token for validation
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$)"
)


def _is_valid_email(email: str) -> bool:
    """Return True if the email matches a basic pattern."""
    return EMAIL_REGEX.match(email) is not None


def change_user_email(query: Dict) -> bool:
    """
    Update a user's email address after verifying CSRF token and input validity.

    Parameters
    ----------
    query : dict
        Dictionary containing the request headers and body.
        Expected keys:
            - "headers": dict with a "csrf-token" key
            - "body": JSON string or dict with keys "user_id" and "new_email"

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    try:
        # 1. CSRF token validation
        headers = query.get("headers", {})
        csrf_token = headers.get("csrf-token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            # Token missing or incorrect
            return False

        # 2. Extract body data (allow dict or JSON string)
        raw_body = query.get("body")
        if isinstance(raw_body, str):
            body_data = json.loads(raw_body)
        elif isinstance(raw_body, dict):
            body_data = raw_body
        else:
            return False

        user_id = str(body_data.get("user_id", "")).strip()
        new_email = body_data.get("new_email", "").strip()

        if not user_id or not new_email:
            return False

        # 3. Validate email format
        if not _is_valid_email(new_email):
            return False

        # 4. Check that the user exists in the database
        if user_id not in database:
            return False

        # 5. Perform the update
        database[user_id]["email"] = new_email
        return True

    except (json.JSONDecodeError, TypeError):
        # Malformed input or type errors
        return False
    except Exception:
        # Catch-all for unexpected errors (logging omitted for brevity)
        return False