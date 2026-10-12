import json
from typing import Dict, Any

# Constants and mock database (to be provided by the surrounding application)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"
database: Dict[str, Any] = {}  # key: user_id (str), value: user data


def remove_user_data(data: Dict[str, Any]) -> bool:
    """
    Remove a user account identified by `user_id` from the in-memory database.

    Parameters
    ----------
    data : dict
        A dictionary representation of an HTTP request. Expected keys:
            - 'headers': a dict containing HTTP headers.
            - 'body'   : a JSON string or dict with the field `user_id`.

    Returns
    -------
    bool
        True if the user was found and removed; False otherwise.

    Notes
    -----
    * The function validates the CSRF token present in the headers.
    * It accepts only string user IDs that exist in `database`.
    * No exception is raised; failures are signaled by returning False.
    """
    try:
        # --- Validate CSRF token ------------------------------------------
        headers = data.get("headers", {})
        csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
        if csrf_token != EXPECTED_CSRF_TOKEN:
            return False  # Invalid or missing CSRF token

        # --- Extract user_id -----------------------------------------------
        body = data.get("body")
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                return False  # Malformed JSON

        user_id = body.get("user_id") if isinstance(body, dict) else None
        if not isinstance(user_id, str):
            return False  # user_id must be a string

        # --- Perform deletion -----------------------------------------------
        if user_id in database:
            del database[user_id]
            return True
        else:
            return False  # User does not exist

    except Exception:
        # Catch-all to prevent leaking sensitive info; return False on any error
        return False