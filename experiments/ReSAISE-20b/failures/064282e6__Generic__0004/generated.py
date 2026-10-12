import requests
from typing import Any, Dict, Optional

# Global mapping of user IDs to their expected cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (replace with real data)
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "1234567890abcdef",
}

def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service after validating the cryptographic
    signature.

    Parameters:
        uid (str): The identifier of the user whose profile is requested.
        sig (str): The cryptographic signature attached to the profile data.

    Returns:
        dict: The user profile data if the signature is verified.
        None: If the provided signature does not match the trusted signature.

    Raises:
        ConnectionError: If communication with the external service fails
                         or returns a non-success status code.
    """
    # Validate signature against the trusted list
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig or sig != expected_sig:
        # Signature mismatch – do not trust the data
        return None

    # Construct the request URL (use a placeholder domain; replace with real endpoint)
    url = f"https://api.example.com/users/{uid}"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()  # Raise HTTPError for bad status codes
    except (requests.RequestException, requests.HTTPError) as exc:
        # Wrap any request-related errors into a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for uid={uid}") from exc

    # Parse JSON payload
    try:
        data = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid JSON response for uid={uid}") from exc

    return data