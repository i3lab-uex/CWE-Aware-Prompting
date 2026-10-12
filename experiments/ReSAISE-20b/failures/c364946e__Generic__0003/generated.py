import json
import requests
from typing import Any, Dict

# Example trusted signatures mapping (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "f1a2b3c4d5e6",
    "bob":   "0123456789ab",
    # add more trusted users as needed
}

def fetch_user_profile(user_id: str, signature: str) -> Any:
    """
    Retrieve a user profile from a remote service and verify its signature.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user whose profile is requested.
    signature : str
        Cryptographic signature that accompanies the returned profile data.

    Returns
    -------
    Any
        The parsed JSON user profile if the signature is valid.
    None
        If the signature does not match the trusted value.

    Raises
    ------
    ConnectionError
        If the remote service cannot be reached or returns a non‑200 status.
    """
    # Ensure we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not expected_sig:
        # Unknown user: treat as untrusted
        return None

    # Verify the supplied signature against the trusted one
    if signature != expected_sig:
        return None

    # Construct the remote URL (example endpoint)
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any request‑level exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    # The response is expected to be JSON
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # Malformed JSON – treat as a connection/format error
        raise ConnectionError(f"Invalid JSON response for user {user_id}") from exc

    return profile_data