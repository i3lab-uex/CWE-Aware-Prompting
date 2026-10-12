import hashlib
import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of profile IDs to expected SHA‑256 hex digests.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (profile_id: expected_digest)
    "user123": "a3f1e2c4d5b6...",
    # Add more trusted profiles here
}

def _compute_digest(data: bytes) -> str:
    """Return the SHA‑256 hex digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its integrity.

    Parameters
    ----------
    profile_id : str
        Identifier of the user whose profile is requested.
    profile_sig : str
        Cryptographic signature (hex digest) provided with the request.

    Returns
    -------
    dict | None
        The decoded JSON profile if signature verification succeeds,
        otherwise ``None``.
    Raises
    ------
    ConnectionError
        If the external service cannot be reached or returns a non‑200 status.
    """
    # 1. Validate the supplied signature against the trusted list
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_sig or expected_sig.lower() != profile_sig.lower():
        # Signature does not match the trusted value
        return None

    # 2. Fetch the profile data from an external endpoint
    url = f"https://api.example.com/profiles/{profile_id}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap lower‑level networking errors into a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for {profile_id}") from exc

    # 3. Verify the integrity of the returned payload
    raw_bytes = response.content
    if _compute_digest(raw_bytes) != expected_sig.lower():
        # Data tampering detected
        return None

    # 4. Return the parsed JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError:
        # Invalid JSON – treat as failure
        return None

    return profile_data