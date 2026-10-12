import re

# Simulated database and CSRF token for demonstration purposes
database = {
    1: {"email": "alice@example.com"},
    2: {"email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

# Regular expression for basic email validation
EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)

def update_user_email(request: dict) -> bool:
    """
    Update the email address of a user in the simulated database.

    Parameters
    ----------
    request : dict
        Must contain:
            - headers: dict, should include 'X-CSRF-Token'
            - body: dict, must contain 'user_id' (int) and 'new_email' (str)

    Returns
    -------
    bool
        True if the email was updated successfully, False otherwise.
    """
    # 1. CSRF protection
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Potential CSRF attack
        return False

    # 2. Extract body parameters
    body = request.get("body", {})
    user_id = body.get("user_id")
    new_email = body.get("new_email")

    # 3. Basic validation
    if not isinstance(user_id, int) or not isinstance(new_email, str):
        return False

    # 4. Email format check
    if not EMAIL_REGEX.match(new_email):
        return False

    # 5. Check user exists
    user_record = database.get(user_id)
    if not user_record:
        return False

    # 6. Update email
    user_record["email"] = new_email.strip()
    return True