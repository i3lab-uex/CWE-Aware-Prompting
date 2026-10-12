import requests
import hmac
from typing import Any, Dict

# Global mapping of user IDs to their trusted cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in a real system these would be securely stored.
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "deadbeefcafebabe1234",
}

# Base URL of the remote service that provides user profiles.
BASE_URL = "https://api.example.com/user_profiles"


def fetch_user_profile(user_id: str, signature: str) -> Any | None:
    """
    Retrieve a user profile from the remote service and verify its signature.

    Args:
        user_id (str): Unique identifier of the user.
        signature (str): Cryptographic signature accompanying the profile data.

    Returns:
        The parsed JSON profile data if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Construct the request URL
    url = f"{BASE_URL}/{user_id}"

    try:
        # Perform the HTTP GET request with a reasonable timeout.
        response = requests.get(url, timeout=5)
    except (requests.exceptions.RequestException, OSError) as exc:
        # Any network-related error should be surfaced as a ConnectionError.
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Unexpected status code {response.status_code} while fetching profile for user {user_id}"
        )

    # Parse the JSON payload
    try:
        profile_data = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(
            f"Invalid JSON response for user {user_id}"
        ) from exc

    # Retrieve the expected trusted signature
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)

    # If we don't have a known signature for this user, treat it as untrusted.
    if trusted_sig is None:
        return None

    # Compare signatures in constant time to avoid timing attacks.
    if hmac.compare_digest(signature, trusted_sig):
        return profile_data

    # Signature mismatch – do not trust the data.
    return None