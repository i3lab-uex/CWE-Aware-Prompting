import json
import hmac
import hashlib
from typing import Dict, Any, Optional

import requests

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here
}

# Remote service endpoint (example)
USER_PROFILE_ENDPOINT = "https://api.example.com/user_profile"


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its cryptographic signature.

    Parameters
    ----------
    u_id : str
        Unique identifier for the user whose profile is being fetched.
    sig_code : str
        Cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If unable to fetch the profile from the remote service.
    """
    # Validate input types
    if not isinstance(u_id, str) or not isinstance(sig_code, str):
        raise TypeError("u_id and sig_code must be strings")

    # Step 1: Fetch the profile from the remote service
    try:
        response = requests.get(
            USER_PROFILE_ENDPOINT,
            params={"u_id": u_id},
            timeout=5.0,          # seconds
            verify=True,          # enforce SSL verification
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Any network or HTTP error results in a ConnectionError
        raise ConnectionError(f"Failed to fetch user profile for '{u_id}': {exc}") from exc

    # Step 2: Parse the JSON response
    try:
        profile = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON from user profile for '{u_id}': {exc}") from exc

    # Step 3: Retrieve the expected signature
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if not expected_sig:
        # No trusted signature available for this user
        return None

    # Step 4: Verify the provided signature using constant‑time comparison
    if not hmac.compare_digest(sig_code, expected_sig):
        # Signature does not match
        return None

    # All checks passed; return the profile
    return profile