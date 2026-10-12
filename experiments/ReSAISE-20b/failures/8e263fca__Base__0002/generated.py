import requests
import hmac

# Global mapping of trusted user IDs to their expected signatures.
TRUSTED_USER_PROFILES = {
    "alice": "5f2e1b3c9d8a4f7e6c0b2d1e3f4a5b6c",
    "bob":   "7c9d8e1f2a3b4c5d6e0f1a2b3c4d5e6f",
    # Add more trusted users as needed
}

def fetch_profile_info(user_ident: str, user_sig: str):
    """
    Fetch a user profile from the remote service and validate its cryptographic signature.

    Parameters
    ----------
    user_ident : str
        The unique identifier for the user whose profile is being fetched.
    user_sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user's profile dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the remote service.
    """
    # URL of the remote user profile endpoint
    url = f"https://api.example.com/users/{user_ident}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Any network related issue is treated as a connection error
        raise ConnectionError(f"Unable to fetch profile for user '{user_ident}'.") from exc

    # Parse the JSON payload
    try:
        profile = response.json()
    except ValueError as exc:
        raise ConnectionError(f"Invalid JSON received for user '{user_ident}'.") from exc

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # No trusted signature known for this user
        return None

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(user_sig, expected_sig):
        return None

    # Signature verified – return the profile
    return profile