import hmac
import hashlib
import json
from typing import Any, Optional

import requests
from requests.exceptions import RequestException

# Example trusted signatures for demonstration purposes.
# In a real application this would be securely stored and accessed.
TRUSTED_USER_PROFILES = {
    "user-1234": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user-5678": "e99a18c428cb38d5f260853678922e03",
    # Add more user IDs and their expected signature hashes here.
}


def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Compare two signatures using a constant‑time comparison to avoid timing attacks.
    The signatures are expected to be hex strings.
    """
    return hmac.compare_digest(provided_sig, expected_sig)


def collect_user_data(uuid: str, sig_hash: str) -> Optional[dict[str, Any]]:
    """
    Fetch a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    uuid : str
        The unique identifier for the user whose profile needs to be fetched.
    sig_hash : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    dict or None
        The parsed user profile if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or connectivity issue.
    """
    # 1. Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not expected_sig:
        # Unknown user – do not proceed with network call
        return None

    if not _verify_signature(sig_hash, expected_sig):
        # Signature mismatch – reject the data
        return None

    # 2. Fetch the profile from a remote service
    # The URL is hypothetical; replace with your actual endpoint.
    url = f"https://api.example.com/users/{uuid}/profile"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any requests exception in a ConnectionError
        raise ConnectionError(f"Unable to fetch profile for user {uuid}") from exc

    # 3. Parse the JSON payload
    try:
        profile = response.json()
    except json.JSONDecodeError as exc:
        # Invalid JSON – treat as a connectivity/formatting issue
        raise ConnectionError(f"Invalid JSON response for user {uuid}") from exc

    return profile