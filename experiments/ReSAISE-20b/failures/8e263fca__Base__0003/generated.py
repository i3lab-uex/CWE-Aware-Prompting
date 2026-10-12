import json
import requests
import hmac
from typing import Any, Dict

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here.
}

def _fetch_remote_profile(user_ident: str) -> Dict[str, Any]:
    """
    Simulate a remote service call to retrieve the user profile.
    Raises ConnectionError if the request fails or returns an error status.
    """
    url = f"https://api.example.com/users/{user_ident}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()  # Assume the service returns JSON.
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to fetch profile for {user_ident}") from exc

def fetch_profile_info(user_ident: str, user_sig: str) -> Dict[str, Any] | None:
    """
    Retrieve a user profile from the remote service and verify its cryptographic signature.

    Parameters:
        user_ident (str): Unique identifier of the user.
        user_sig (str): Cryptographic signature supplied with the profile.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Step 1: Retrieve the expected signature for this user, if any.
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # No trusted signature known for this user.
        return None

    # Step 2: Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(user_sig, expected_sig):
        # Signature mismatch – do not trust the profile.
        return None

    # Step 3: Fetch the profile from the remote service.
    profile = _fetch_remote_profile(user_ident)

    # Optionally, you could perform additional checks here (e.g., schema validation).

    return profile