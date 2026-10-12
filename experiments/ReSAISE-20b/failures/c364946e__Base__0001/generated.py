import requests
import hmac
from typing import Optional

# Global dictionary mapping user IDs to trusted signatures (hex-encoded)
TRUSTED_USER_PROFILES = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e3afed0047b08059d0fada10f400c1e5",
    # Add more trusted user signatures here
}

def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Verify that the provided signature matches the expected one using
    constant‑time comparison to mitigate timing attacks.
    """
    # Ensure both signatures are the same length before comparing
    if len(provided_sig) != len(expected_sig):
        return False
    # Use hmac.compare_digest for constant‑time comparison
    return hmac.compare_digest(provided_sig, expected_sig)

def fetch_user_profile(user_id: str, signature: str) -> Optional[dict]:
    """
    Retrieve a user profile from a remote service and verify its signature.

    Args:
        user_id (str): The unique identifier of the user.
        signature (str): The cryptographic signature accompanying the profile data.

    Returns:
        dict: The user profile data if the signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If the profile could not be fetched from the remote service.
    """
    # Validate that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if expected_sig is None:
        # No trusted signature known for this user; refuse to verify
        return None

    if not _verify_signature(signature, expected_sig):
        # Signature does not match the trusted value
        return None

    # Construct the URL for fetching the user profile
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap any request-related error in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    try:
        # Assume the remote service returns JSON
        profile_data = response.json()
    except ValueError as exc:
        # Response was not valid JSON
        raise ConnectionError(f"Invalid response format for user {user_id}") from exc

    return profile_data