import requests
from typing import Any, Dict, Optional

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "abcde12345",
    "user456": "fghij67890",
    # Add more trusted user IDs and signatures here.
}

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote service and validate its cryptographic signature.

    Parameters
    ----------
    u_id : str
        The unique identifier for the user whose profile is being fetched.
    sig_code : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Build the request URL.  In a real system this would be configurable.
    url = f"https://api.example.com/users/{u_id}"

    try:
        # Perform the HTTP GET with a timeout to avoid hanging indefinitely.
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Any request-related exception is treated as a connection error.
        raise ConnectionError(f"Failed to fetch user profile for {u_id}") from exc

    try:
        # Parse the JSON response.  If it is not valid JSON, treat as a connection error.
        profile = response.json()
    except ValueError as exc:
        raise ConnectionError(f"Invalid JSON received for user {u_id}") from exc

    # Validate the signature against the trusted mapping.
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # The user ID is not known to be trusted.
        return None

    if expected_sig != sig_code:
        # Signature mismatch: do not trust the profile.
        return None

    return profile