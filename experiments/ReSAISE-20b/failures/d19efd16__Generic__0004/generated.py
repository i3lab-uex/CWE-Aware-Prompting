import json
import hashlib
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException


# Global mapping of user IDs to their trusted profile signatures (hex strings)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries:
    # "user123": "5f2d9c1a... (hex signature)",
}

def _compute_signature(data: Any) -> str:
    """
    Compute a SHA‑256 hash of the JSON representation of *data*.
    The resulting hex string is used as a signature.
    """
    json_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(json_bytes).hexdigest()


def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its integrity.

    Parameters
    ----------
    profile_id : str
        Identifier of the user whose profile is requested.
    profile_sig : str
        Signature that accompanies the profile data.

    Returns
    -------
    dict or None
        The profile data if signature verification succeeds; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the HTTP request to fetch the profile fails.
    """
    # 1. Fetch the profile data from the external service
    url = f"https://api.example.com/profiles/{profile_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request‑related exception in a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile {profile_id}") from exc

    # 2. Parse the JSON payload
    try:
        payload = response.json()
    except ValueError as exc:  # invalid JSON
        raise ConnectionError(f"Invalid JSON response for profile {profile_id}") from exc

    # Expected payload structure: {"data": {...}, "signature": "..."}
    if not isinstance(payload, dict) or "data" not in payload:
        raise ConnectionError(f"Malformed response for profile {profile_id}")

    data = payload["data"]

    # 3. Verify the signature that came with the response
    computed_sig = _compute_signature(data)
    if computed_sig != profile_sig:
        # Signature does not match the data – reject
        return None

    # 4. Cross‑check against the globally trusted signature (if present)
    trusted_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if trusted_sig and computed_sig != trusted_sig:
        # The signature is not the one we trust for this user
        return None

    # 5. All checks passed – return the profile data
    return data