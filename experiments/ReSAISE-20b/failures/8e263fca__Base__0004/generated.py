import secrets
from typing import Any, Dict, Optional

# Global mapping of trusted user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "abcde12345fghij67890klmnop",
    "alice":   "09876zyxwvu54321tsrqponmlk",
    # Add more trusted users as needed.
}

def _remote_fetch_profile(user_ident: str) -> Dict[str, Any]:
    """
    Simulates fetching a user profile from a remote service.
    Raises ConnectionError if the remote fetch fails.

    In a real implementation, this would perform an HTTP request or similar.
    """
    # For demonstration purposes, we'll pretend that the remote service
    # returns a simple profile dictionary. In practice this function would
    # be replaced with actual network code.
    if user_ident not in TRUSTED_USER_PROFILES:
        # Simulate a 404 or service error.
        raise ConnectionError(f"Unable to fetch profile for user {user_ident}")

    # Dummy profile data
    return {
        "id": user_ident,
        "name": "Example User",
        "email": f"{user_ident}@example.com"
    }

def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a user profile from a remote service and verifies its cryptographic
    signature against the expected value.

    Parameters:
        user_ident (str): Unique identifier of the user.
        user_sig (str): Cryptographic signature associated with the profile.

    Returns:
        dict: The user profile if the signature matches.
        None: If the signature does not match.

    Raises:
        ConnectionError: If fetching the profile from the remote service fails.
    """
    # 1. Retrieve expected signature for this user, if any
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # Unknown user: treat as untrusted
        return None

    # 2. Verify the signature using constant‑time comparison to avoid timing attacks
    if not secrets.compare_digest(user_sig, expected_sig):
        # Signature mismatch: do not trust the data
        return None

    # 3. Fetch the profile from the remote service
    try:
        profile = _remote_fetch_profile(user_ident)
    except ConnectionError as exc:
        # Propagate the connection error
        raise

    # 4. Return the profile only if we reached this point
    return profile