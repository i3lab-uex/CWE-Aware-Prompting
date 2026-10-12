import json
import hmac
import requests
from typing import Optional

# Example trusted signatures for demonstration purposes.
TRUSTED_USER_PROFILES = {
    "user123": "sha256:abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx2345yzab6789cdef0123",
    "user456": "sha256:1234abcd5678efgh9012ijkl3456mnop7890qrst0123uvwx4567yzab8901cdef",
    # ... add more trusted user signatures here ...
}

# Base URL for the remote system that hosts user profiles.
BASE_PROFILE_URL = "https://api.example.com/users"


def access_user_details(identifier: str, crypt_sig: str) -> Optional[dict]:
    """
    Fetch a user profile from the remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique user identifier.
    crypt_sig : str
        The cryptographic signature received alongside the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved due to a network or server error.
    """
    # Construct request URL
    url = f"{BASE_PROFILE_URL}/{identifier}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as exc:
        # Propagate connectivity issues
        raise ConnectionError(f"Failed to fetch profile for {identifier}") from exc

    # Parse the JSON payload
    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON received for {identifier}") from exc

    # Verify the signature using constant‑time comparison to mitigate timing attacks.
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # No trusted signature known for this user; treat as invalid.
        return None

    if not hmac.compare_digest(expected_sig, crypt_sig):
        # Signature mismatch
        return None

    # All checks passed; return the profile data.
    return data