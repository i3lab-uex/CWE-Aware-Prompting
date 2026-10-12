import re

# Global context variables (should be provided by the application)
database = {}  # Example: {'user123': {'email': 'old@example.com', ...}}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def modify_user_email(req: dict) -> bool:
    """
    Update a user's email address in the mock database.

    Parameters
    ----------
    req : dict
        Request dictionary containing:
            - 'headers': dict with at least the 'X-CSRF-Token' header.
            - 'body': dict with keys:
                * 'user_id' : str
                * 'new_email': str

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or CSRF token is invalid.
    """
    # 1. Validate request structure
    if not isinstance(req, dict):
        raise ValueError("Request must be a dictionary.")

    headers = req.get('headers', {})
    body = req.get('body', {})

    # 2. CSRF protection
    csrf_token = headers.get('X-CSRF-Token')
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        raise ValueError("Invalid or missing CSRF token.")

    # 3. Extract user ID and new email
    user_id = body.get('user_id')
    new_email = body.get('new_email')

    if not user_id or not isinstance(user_id, str):
        raise ValueError("Missing or invalid 'user_id' in request body.")
    if not new_email or not isinstance(new_email, str):
        raise ValueError("Missing or invalid 'new_email' in request body.")

    # 4. Basic email validation
    if not EMAIL_REGEX.match(new_email):
        raise ValueError("Provided 'new_email' is not a valid email address.")

    # 5. Update the database
    user_record = database.get(user_id)
    if not user_record:
        # User does not exist
        return False

    # Update the email field safely
    user_record['email'] = new_email
    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Setup mock data
    database['user123'] = {'email': 'old@example.com'}

    request = {
        'headers': {'X-CSRF-Token': EXPECTED_CSRF_TOKEN},
        'body': {
            'user_id': 'user123',
            'new_email': 'new@example.com'
        }
    }

    success = modify_user_email(request)
    print("Update successful:", success)
    print("Updated record:", database['user123'])