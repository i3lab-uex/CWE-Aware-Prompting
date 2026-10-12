import requests
from typing import Any, Dict, Optional
import hmac

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "a3f5c2d4e6b8",
    "user2": "1d9a3f7c0e4b",
    # Add more trusted users here.
}

def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile is being fetched.
    sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict or None
        The user profile if the signature matches a trusted value; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # 1. Validate that we have a trusted signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature known for this user.
        return None

    # 2. Perform a constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(sig, expected_sig):
        # Signature does not match; reject the profile.
        return None

    # 3. Fetch the profile from the remote service.
    url = f"https://example.com/api/users/{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as exc:
        # Wrap any network or HTTP error in a ConnectionError.
        raise ConnectionError(f"Unable to fetch profile for user {uid}") from exc

    # 4. Parse the JSON payload.
    try:
        profile = response.json()
    except ValueError as exc:
        # Invalid JSON payload; treat it as a connection error.
        raise ConnectionError(f"Invalid response for user {uid}") from exc

    return profile