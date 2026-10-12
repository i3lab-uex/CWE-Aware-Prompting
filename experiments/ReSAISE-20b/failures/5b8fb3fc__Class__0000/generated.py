import urllib.request
import json
import hmac
from typing import Optional, Dict

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in real use these would be securely stored.
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "0j9i8h7g6f5e4d3c2b1a",
}

# Base URL of the remote service providing user profiles.
REMOTE_SERVICE_BASE_URL = "https://api.example.com/user_profiles"


def _fetch_remote_profile(uid: str) -> dict:
    """
    Fetch the user profile from the remote service.

    Raises ConnectionError if the request fails.
    """
    url = f"{REMOTE_SERVICE_BASE_URL}/{uid}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status != 200:
                raise ConnectionError(f"Unexpected status code {response.status}")
            data = response.read()
            return json.loads(data)
    except urllib.error.URLError as exc:
        raise ConnectionError(f"Failed to fetch profile for {uid}: {exc}") from exc


def retrieve_user_profile(uid: str, sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from the remote service and verify its signature.

    Parameters
    ----------
    uid : str
        Unique identifier of the user.
    sig : str
        Cryptographic signature provided with the profile.

    Returns
    -------
    dict | None
        The user profile if the signature matches a trusted value, otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Step 1: Fetch the profile
    profile = _fetch_remote_profile(uid)

    # Step 2: Retrieve expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature known for this user
        return None

    # Step 3: Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Signature matches; return the profile
    return profile