import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to their correct cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "alice": "f4b1c2d3e5a7f8g9h0i1j2k3l4m5n6o7",
    "bob":   "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    # ... more entries ...
}

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique identifier for the user whose profile needs to be fetched.
    crypt_sig : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the user profile cannot be fetched due to connectivity issues.
    """
    # Construct the URL for the remote API endpoint
    url = f"https://api.example.com/users/{identifier}"

    try:
        # Perform the HTTP GET request with a reasonable timeout
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Any network/HTTP error is treated as a connectivity problem
        raise ConnectionError(f"Failed to fetch user profile for '{identifier}': {exc}") from exc

    # Parse the JSON response
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # Malformed JSON is considered a connectivity/content error
        raise ConnectionError(f"Invalid JSON response for user '{identifier}': {exc}") from exc

    # Verify the provided signature against the trusted value
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # Unknown user ID: treat as invalid signature
        return None

    if crypt_sig == expected_sig:
        return profile_data
    else:
        # Signature mismatch; do not trust the data
        return None