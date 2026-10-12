import requests
from typing import Any, Dict, Optional

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "e3b0c44298fc1c149afbf4c8996fb924",
    "bob":   "9f86d081884c7d659a2feaa0c55ad015",
    # Add more trusted users here.
}

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        Unique user ID to fetch.
    crypt_sig : str
        Cryptographic signature provided with the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity issues.
    """
    # URL of the remote service (example placeholder).
    url = f"https://api.example.com/users/{identifier}"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError) as exc:
        # Wrap lower‑level errors into a generic ConnectionError.
        raise ConnectionError(f"Failed to fetch user profile for {identifier}") from exc

    try:
        profile_data = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid response format for {identifier}") from exc

    # Verify the cryptographic signature against the trusted mapping.
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # No trusted signature known for this user; treat as invalid.
        return None

    if crypt_sig != expected_sig:
        # Signature mismatch – data is not trusted.
        return None

    return profile_data