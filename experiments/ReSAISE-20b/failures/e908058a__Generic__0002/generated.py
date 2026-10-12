import json
from typing import Any, Dict, Optional

try:
    import requests  # type: ignore[import]
except Exception as exc:
    raise ImportError("The 'requests' library is required for network operations.") from exc

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in a real system these would be populated from secure storage.
    "user-123": "a1b2c3d4e5f6g7h8i9j0",
    "user-456": "z9y8x7w6v5u4t3s2r1q0",
    # ...
}


def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote system and verify its signature.

    Parameters
    ----------
    uuid : str
        The unique identifier of the user whose profile is to be fetched.
    sig_hash : str
        The cryptographic signature supplied with the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or connectivity issue.
    """
    # Validate input types
    if not isinstance(uuid, str) or not isinstance(sig_hash, str):
        raise TypeError("Both 'uuid' and 'sig_hash' must be strings.")

    # Construct the request URL
    url = f"https://api.example.com/users/{uuid}"

    try:
        # Perform the GET request with a reasonable timeout
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.ConnectionError,
            requests.Timeout,
            requests.HTTPError) as exc:
        # Wrap any request-related exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch user profile for '{uuid}'.") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the response isn't valid JSON, treat it as a failure to fetch data
        raise ConnectionError(f"Invalid response format for user '{uuid}'.") from exc

    # Retrieve the expected signature for this UUID
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)

    # If the user is unknown or the signature does not match, return None
    if expected_sig is None:
        # Unknown user; signature cannot be verified
        return None

    if sig_hash != expected_sig:
        # Signature mismatch – data is untrusted
        return None

    # All checks passed; return the profile data
    return profile_data