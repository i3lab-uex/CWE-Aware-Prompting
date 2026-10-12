import re
from typing import Dict, Any

# Simulated global database and CSRF token for the example.
database: Dict[int, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

# Regular expression for a simple email validation
EMAIL_REGEX = re.compile(
    r"(^[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*"
    r"@([A-Za-z0-9]([-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$)"
)

def change_user_email(new_request: Dict[str, Any]) -> bool:
    """
    Update a user's email address in the simulated database.

    Parameters
    ----------
    new_request : dict
        Incoming request containing 'headers' and 'body'. The body must include:
            - user_id : int
            - new_email : str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    try:
        headers = new_request["headers"]
        body = new_request["body"]

        # CSRF token validation
        csrf_token = headers.get("X-CSRF-Token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False

        # Extract and validate input data
        user_id = body.get("user_id")
        new_email = body.get("new_email")

        if not isinstance(user_id, int) or not isinstance(new_email, str):
            return False

        if not EMAIL_REGEX.match(new_email):
            return False

        # Ensure the user exists in the database
        if user_id not in database:
            return False

        # Update the email address safely
        database[user_id]["email"] = new_email.strip()
        return True

    except (KeyError, AttributeError):
        # Missing expected keys or wrong data structure
        return False
    except Exception:
        # Catch-all for unforeseen errors (logging can be added in real usage)
        return False