import json
from typing import Any, Optional

import requests
import hmac

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES = {
    # Example entries:
    "alice": "5f2d7c3e9a1b4e6f8c0d1e2f3a4b5c6d",
    "bob":   "9a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d",
    # Add real entries here.
}


def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Compare two signatures using a timing‑attack resistant comparison.
    """
    # Ensure both are bytes for compare_digest
    return hmac.compare_digest(
        provided_sig.encode("utf-8"), expected_sig.encode("utf-8")
    )


def retrieve_user_info(uid: str, sig: str) -> Optional[Any]:
    """
    Fetch a user profile from a remote system and verify its signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user.
    sig : str
        The cryptographic signature that accompanies the profile data.

    Returns
    -------
    dict or list or None
        The parsed JSON profile if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the HTTP request fails due to connectivity issues.
    """
    # 1. Verify that we have a trusted signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No known signature for this user; treat as untrusted.
        return None

    if not _verify_signature(sig, expected_sig):
        # Signature mismatch – do not trust the data.
        return None

    # 2. Fetch the profile from the remote service.
    url = f"https://api.example.com/users/{uid}"
    try:
        resp = requests.get(url, timeout=5)  # seconds
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any request exception to a ConnectionError.
        raise ConnectionError(f"Failed to fetch user profile for {uid}") from exc

    # 3. Return the JSON payload.
    try:
        return resp.json()
    except json.JSONDecodeError:
        # Malformed JSON – treat as failure.
        return None