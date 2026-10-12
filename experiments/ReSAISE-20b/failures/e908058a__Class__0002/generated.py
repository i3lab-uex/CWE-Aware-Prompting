import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "user-123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user-456": "e99a18c428cb38d5f260853678922e03",
    # ... more entries
}

def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    return hmac.compare_digest(val1.encode(), val2.encode())

def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    uuid : str
        The unique identifier of the user whose profile is to be fetched.
    sig_hash : str
        The cryptographic signature that accompanies the returned profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is verified; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved due to a network or connectivity problem.
    """
    # Define the endpoint URL. In production this would be configurable.
    url = f"https://api.example.com/users/{uuid}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as exc:
        # Any network-related issue is treated as a connectivity problem.
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc

    # Parse the JSON payload. Assume it contains a 'profile' field.
    try:
        data = response.json()
        profile = data.get("profile")
    except (ValueError, AttributeError) as exc:
        # Malformed JSON or unexpected structure.
        raise ConnectionError(f"Invalid response format for user {uuid}") from exc

    # Retrieve the expected signature from the trusted mapping.
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not expected_sig:
        # If we have no record of this user, we cannot trust the data.
        return None

    # Perform a constant-time comparison to mitigate timing attacks.
    if not _constant_time_compare(sig_hash, expected_sig):
        # Signature mismatch: data is not trusted.
        return None

    # If we reach this point, the signature is valid and the profile can be returned.
    return profile