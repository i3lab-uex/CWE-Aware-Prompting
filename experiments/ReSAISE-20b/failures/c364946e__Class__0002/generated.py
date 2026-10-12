import json
from typing import Any, Dict, Optional

import requests

# Global mapping of user IDs to their trusted signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in a real system these would be populated from
    # a secure source (e.g., environment variable, config file,
    # or a secrets manager).
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
    # ... more entries
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote service and verify its authenticity.

    Parameters
    ----------
    user_id : str
        Unique identifier of the user whose profile is requested.
    signature : str
        Cryptographic signature accompanying the returned profile data.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature matches a trusted value,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile could not be fetched from the remote service.
    """
    # Step 1: Verify that we have a trusted signature for this user
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not trusted_sig:
        # Unknown user – do not trust any data we might receive
        return None

    if signature != trusted_sig:
        # Signature does not match – reject the data
        return None

    # Step 2: Fetch the profile from a remote service over HTTPS
    url = f"https://api.example.com/users/{user_id}/profile"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Any network or HTTP error is treated as a connection failure
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    # Step 3: Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # Invalid JSON – treat as a failure to fetch valid data
        raise ConnectionError(f"Invalid JSON received for user {user_id}") from exc

    # Optional: perform schema validation here if desired
    return profile_data