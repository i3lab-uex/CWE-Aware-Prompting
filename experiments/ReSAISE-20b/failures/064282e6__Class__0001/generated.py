import json
import hmac
from typing import Any, Dict

import requests  # pip install requests if missing

# Example trusted signature mapping. In a real system this would be securely stored.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "9e107d9d372bb6826bd81d3542a419d6",
    # ... other users
}

def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Compare signatures using a constant‑time comparison to mitigate timing attacks.
    """
    return hmac.compare_digest(provided_sig, expected_sig)

def retrieve_user_data(uid: str, sig: str) -> Any:
    """
    Fetch a user profile from an external service and verify its authenticity.

    Parameters
    ----------
    uid : str
        Identifier of the target user.
    sig : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    Any
        The user profile data if signature verification succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the external service cannot be reached or returns an unexpected status code.
    """
    # Ensure we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature known – cannot validate
        return None

    if not _verify_signature(sig, expected_sig):
        # Signature mismatch – do not trust the data
        return None

    # Build the request URL (the real endpoint would be environment‑specific)
    url = f"https://api.example.com/user/{uid}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, ValueError) as exc:
        # Wrap any network/HTTP error into a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for uid={uid}") from exc

    try:
        data = response.json()
    except json.JSONDecodeError:
        # The service returned non‑JSON – treat as failure
        return None

    return data