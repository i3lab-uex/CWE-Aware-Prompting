import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests  # pip install requests

# Global mapping of user identifiers to their trusted signature
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "6cb75f652a9b52798eb6cf2201057c73",
}

# Base URL of the external service providing user profiles
EXTERNAL_SERVICE_URL = "https://api.example.com/user"


def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Compare two signatures in a timing‑safe manner.
    """
    return hmac.compare_digest(provided_sig.encode(), expected_sig.encode())


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its cryptographic signature.

    Parameters
    ----------
    user_identifier : str
        Identifier of the target user.
    user_signature : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict or None
        The user profile data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Fetch expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_identifier)
    if not expected_sig:
        # No trusted signature known for this user
        return None

    # Verify the provided signature against the expected one
    if not _verify_signature(user_signature, expected_sig):
        return None

    # At this point the signature is considered valid; fetch profile data
    try:
        response = requests.get(f"{EXTERNAL_SERVICE_URL}/{user_identifier}", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Any network or HTTP error is treated as a connection failure
        raise ConnectionError(f"Failed to retrieve profile for user '{user_identifier}'") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError:
        # Malformed JSON – treat as a failure to retrieve valid data
        raise ConnectionError(f"Invalid JSON response for user '{user_identifier}'")

    return profile_data