import hmac

# Predefined CSRF token used by the application
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Delete a user account identified by the 'user_id' field in input_request['body'].
    
    Parameters
    ----------
    input_request : dict
        A dictionary representing an HTTP request, containing:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body': dict with a 'user_id' key (int or str).
    database : dict
        An in-memory dictionary simulating the user database. Keys are user IDs.
    
    Returns
    -------
    bool
        True if the account was deleted, False otherwise.
    
    Notes
    -----
    * CSRF protection: The function verifies that the request includes a valid
      CSRF token using constant‑time comparison to mitigate timing attacks.
    * Validation: The function checks for missing keys, ensures the user ID is
      present in the database before deletion, and returns False if any check fails.
    """
    
    # 1. Validate presence of required parts
    headers = input_request.get("headers")
    body = input_request.get("body")
    
    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False
    
    # 2. CSRF token verification
    token = headers.get("X-CSRF-Token")
    if not isinstance(token, str):
        return False
    
    # Use constant-time comparison to avoid timing attacks
    if not hmac.compare_digest(token, EXPECTED_CSRF_TOKEN):
        return False
    
    # 3. Extract user ID and ensure it exists in the database
    user_id = body.get("user_id")
    
    if user_id is None:
        return False
    
    # Normalise user ID to string for dictionary key consistency
    try:
        normalized_id = str(user_id)
    except Exception:
        return False
    
    if normalized_id not in database:
        return False
    
    # 4. Delete the user entry
    try:
        del database[normalized_id]
    except Exception:
        return False
    
    return True