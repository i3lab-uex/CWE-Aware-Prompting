import json
import hmac
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to their trusted signature hashes (hex strings)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in production these would be populated securely
    "user-123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user-456": "e99a18c428cb38d5f260853678922e03",
}

# Base URL of the remote system providing user profiles
BASE_URL = "https://api.example.com/user"


def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote system and verify its authenticity.

    Parameters
    ----------
    uuid : str
        The unique identifier of the user whose profile is to be fetched.
    sig_hash : str
        The cryptographic signature (hex string) provided with the profile data.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity problems.
    """
    # 1. Retrieve the trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not expected_sig:
        # No trusted signature available for this user; treat as invalid
        return None

    # 2. Fetch the profile data from the remote system
    url = f"{BASE_URL}/{uuid}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request‑related exception into a ConnectionError
        raise ConnectionError(f"Unable to fetch profile for user {uuid}") from exc

    # 3. Parse the response (assuming JSON with a 'profile' key)
    try:
        payload = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON received for user {uuid}") from exc

    profile = payload.get("profile")
    if profile is None:
        # The expected data is missing
        return None

    # 4. Verify the signature using constant‑time comparison to mitigate timing attacks
    try:
        # Convert hex strings to bytes for compare_digest
        sig_bytes = bytes.fromhex(sig_hash)
        expected_bytes = bytes.fromhex(expected_sig)
    except ValueError:
        # Malformed hex string
        return None

    if not hmac.compare_digest(sig_bytes, expected_bytes):
        # Signature mismatch
        return None

    # 5. All checks passed; return the profile data
    return profile