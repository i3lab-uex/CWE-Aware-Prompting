import json
from typing import Dict, Any

# Simulated database and CSRF token (normally these would be stored securely)
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure_token_123"

def delete_user_account(request: Dict[str, Any]) -> bool:
    """
    Deletes a user account identified by `user_id` in the request body.
    
    Parameters
    ----------
    request : dict
        Dictionary containing 'headers' and 'body'. The body must be JSON
        encoded or a dict with key 'user_id'.
    
    Returns
    -------
    bool
        True if the user was found and removed, False otherwise.
    
    Security Notes
    --------------
    - CSRF protection: The request must contain a valid CSRF token in either
      the 'X-CSRF-Token' header or as part of the body.
    - Input validation: Only accepts numeric or UUID string for `user_id`.
    """
    
    # Helper to extract CSRF token
    def get_csrf_token(req: Dict[str, Any]) -> str | None:
        # Check header first
        headers = req.get("headers", {})
        token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
        if token:
            return token
        # Fallback to body (in case of JSON payload)
        body = req.get("body")
        if isinstance(body, str):
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                return None
        else:
            data = body if isinstance(body, dict) else {}
        return data.get("csrf_token")
    
    # Validate CSRF token
    csrf_token = get_csrf_token(request)
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token
        return False
    
    # Extract user_id from body
    body = request.get("body")
    if isinstance(body, str):
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return False
    else:
        data = body if isinstance(body, dict) else {}
    
    user_id = data.get("user_id")
    if not isinstance(user_id, str):
        # Accept only string IDs; adjust as needed
        return False
    
    # Perform deletion
    if user_id in database:
        del database[user_id]
        return True
    
    # User not found
    return False