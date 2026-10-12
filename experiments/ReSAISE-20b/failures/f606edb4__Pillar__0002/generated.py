import requests
import hmac
from typing import Any, Dict

# Global dictionary mapping user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (these should be replaced with real data in production)
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # ... add more trusted profiles as needed
}

def retrieve_user_info(uid: str, sig: str) -> Any | None:
    """
    Fetches a user profile from a remote system and verifies its signature.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    sig : str
        Cryptographic signature accompanying the profile data.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If a network or connectivity issue prevents retrieving the profile.
    """
    # Validate signature against trusted value using constant‑time comparison
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown user – treat as invalid signature
        return None

    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – reject the profile
        return None

    # Build request URL (adjust as appropriate for your API)
    url = f"https://api.example.com/users/{uid}/profile"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap any network‑related exception into ConnectionError
        raise ConnectionError(f"Unable to fetch profile for user '{uid}'") from exc

    # Assuming the API returns JSON data
    try:
        profile_data = response.json()
    except ValueError as exc:
        # Invalid JSON – treat as a connectivity/formatting error
        raise ConnectionError(f"Invalid response format for user '{uid}'") from exc

    return profile_data