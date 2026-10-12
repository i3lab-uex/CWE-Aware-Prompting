import requests
from typing import Any, Dict, Optional

# Example trusted signatures for demonstration purposes.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "abc123signature",
    "user2": "def456signature",
    # Add more user IDs and their expected signatures here.
}

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile is requested.
    sig : str
        The cryptographic signature provided alongside the profile data.

    Returns
    -------
    dict or None
        The user profile dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the remote request fails due to connectivity issues.
    """
    # Verify that the provided signature matches the trusted one for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None or sig != expected_sig:
        # Either the user is unknown or the signature does not match
        return None

    # Construct the URL for the remote user profile endpoint.
    url = f"https://api.example.com/users/{uid}"

    try:
        response = requests.get(url, timeout=5.0)
        # Raise an HTTPError for bad responses (4xx/5xx)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any request-related exception into a ConnectionError
        raise ConnectionError(f"Failed to retrieve user profile for {uid}") from exc

    # Assuming the API returns JSON-encoded profile data.
    try:
        profile = response.json()
    except ValueError as exc:  # includes JSONDecodeError
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    return profile