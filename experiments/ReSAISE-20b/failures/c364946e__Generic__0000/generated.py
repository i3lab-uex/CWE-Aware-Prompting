import requests
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to the trusted signature for their profile data.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in production these would be populated from a secure source.
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # ...
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    user_id : str
        Unique identifier of the user whose profile is requested.
    signature : str
        Cryptographic signature accompanying the fetched data.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature matches a trusted value,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile could not be retrieved from the remote service.
    """
    # Endpoint for fetching user profiles (replace with actual URL).
    url = f"https://api.example.com/users/{user_id}"

    try:
        # Perform the HTTP GET request with a reasonable timeout.
        response = requests.get(url, timeout=5.0)
    except (requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException) as exc:
        # Wrap any request-related exception in a ConnectionError.
        raise ConnectionError(f"Failed to fetch profile for user '{user_id}': {exc}") from exc

    # If the HTTP status code is not 200, treat it as a failure.
    if response.status_code != 200:
        raise ConnectionError(
            f"Unexpected status {response.status_code} when fetching profile for user '{user_id}'."
        )

    # Parse JSON; if parsing fails, treat it as a malformed response.
    try:
        profile_data = response.json()
    except ValueError as exc:  # includes json.decoder.JSONDecodeError
        raise ConnectionError(f"Invalid JSON response for user '{user_id}': {exc}") from exc

    # Verify that the provided signature matches the trusted one for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if expected_sig is None:
        # No trusted signature known for this user; cannot verify.
        return None

    if signature != expected_sig:
        # Signature mismatch – data may have been tampered with.
        return None

    # All checks passed; return the profile data.
    return profile_data