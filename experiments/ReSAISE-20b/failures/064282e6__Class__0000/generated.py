import requests
import hmac
import hashlib
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to the expected HMAC-SHA256 signature of their profile data.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries:
    # "user123": "5f2c... (hex signature)",
}

def _constant_time_compare(val1: str, val2: str) -> bool:
    """Return True if the two strings are equal, using a constant‑time comparison."""
    return hmac.compare_digest(val1.encode(), val2.encode())

def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its signature.

    Parameters
    ----------
    uid : str
        Identifier of the user whose profile is being fetched.
    sig : str
        Cryptographic signature attached to the retrieved profile data.

    Returns
    -------
    dict or None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # 1. Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature known – cannot trust the data
        return None

    # 2. Retrieve the profile from an external service
    try:
        response = requests.get(
            f"https://api.example.com/users/{uid}/profile",
            timeout=5,  # seconds
        )
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise ConnectionError(f"Failed to retrieve profile for uid {uid}") from exc

    # 3. Extract the profile data as a JSON object
    try:
        profile_data = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid response format for uid {uid}") from exc

    # 4. Validate the provided signature against the expected one
    if not _constant_time_compare(sig, expected_sig):
        # Signature does not match – reject the data
        return None

    # 5. All checks passed; return the profile data
    return profile_data