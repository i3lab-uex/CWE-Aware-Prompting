import json
import hmac
import hashlib
import requests
from typing import Any, Dict, Optional

# Example trusted signatures mapping (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    # Add actual trusted signatures here
}

# Base URL for the external user profile service.
BASE_PROFILE_URL = "https://api.example.com/profiles"

def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its cryptographic signature.

    Parameters
    ----------
    profile_id : str
        Identifier for the targeted user.
    profile_sig : str
        Hex-encoded cryptographic signature attached to the profile data.

    Returns
    -------
    dict or None
        The user profile data if signature verification succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Validate that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if expected_sig is None:
        # Unknown user – do not attempt to fetch
        return None

    # Perform a constant‑time comparison of the supplied signature and the expected one
    if not hmac.compare_digest(profile_sig.lower(), expected_sig.lower()):
        # Signature mismatch – do not trust the data
        return None

    # Build request URL
    url = f"{BASE_PROFILE_URL}/{profile_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Any network or HTTP error is treated as a connection failure
        raise ConnectionError(f"Failed to retrieve profile for {profile_id}") from exc

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        # Malformed JSON – treat as a failure to retrieve valid data
        raise ConnectionError(f"Invalid JSON response for {profile_id}") from exc

    # Additional sanity checks on the returned data can be added here
    return data