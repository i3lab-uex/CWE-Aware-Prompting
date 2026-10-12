import requests
import hmac
from typing import Optional, Dict

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored).
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "0z9y8x7w6v5u4t3s2r1q",
}

# Base URL of the remote service that hosts user profiles.
REMOTE_SERVICE_URL = "https://api.example.com/user_profiles"


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the remote service and validate its signature.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    sig : str
        Cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # 1. Verify that we have a trusted signature for this user ID.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown user ID; treat as untrusted.
        return None

    # 2. Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(sig, expected_sig):
        # Signature does not match; do not trust the data.
        return None

    # 3. Fetch the profile from the remote service.
    try:
        response = requests.get(f"{REMOTE_SERVICE_URL}/{uid}", timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap any network or HTTP error into a ConnectionError.
        raise ConnectionError(f"Failed to retrieve profile for user {uid}") from exc

    # 4. Parse the JSON response.
    try:
        profile = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    # 5. Final sanity check: ensure the returned profile contains expected keys.
    if not isinstance(profile, dict) or "uid" not in profile:
        return None

    return profile