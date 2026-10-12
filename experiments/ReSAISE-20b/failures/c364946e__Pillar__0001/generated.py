import requests
import hmac
from typing import Optional

# Global dictionary mapping user IDs to their trusted signatures
TRUSTED_USER_PROFILES = {
    # Example entries; replace with real data in production
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "0123456789abcdef1234",
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[dict]:
    """
    Retrieve a user profile from the remote service and verify its signature.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user whose profile needs to be fetched.
    signature : str
        The cryptographic signature accompanying the user profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the user profile could not be fetched from the remote service.
    """
    # Validate input types early
    if not isinstance(user_id, str) or not isinstance(signature, str):
        raise TypeError("user_id and signature must be strings")

    # Construct the request URL (example; adjust to real endpoint)
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Wrap any request-related exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for {user_id}") from exc

    # Parse the JSON payload
    try:
        data = response.json()
    except ValueError as exc:
        # Malformed JSON is treated as a connection issue
        raise ConnectionError(f"Invalid JSON response for {user_id}") from exc

    # Retrieve the trusted signature for this user
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if trusted_sig is None:
        # No known signature for this user; cannot trust the data
        return None

    # Use constant‑time comparison to avoid timing attacks (CWE‑693)
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # All checks passed; return the profile data
    return data