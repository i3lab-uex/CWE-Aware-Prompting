import hmac
import hashlib
import requests
from typing import Optional

# Global dictionary mapping user IDs to their correct signatures.
TRUSTED_USER_PROFILES = {
    # Example entries; replace with real values in production
    "user1": "a3f5c9d2e6b7... (hex signature)",
    "user2": "b1c4d8e9f0a1... (hex signature)",
}

# URL template for the remote system that returns user profiles in JSON format.
USER_PROFILE_ENDPOINT = "https://api.example.com/users/{uid}"


def _verify_signature(uid: str, received_sig: str) -> bool:
    """
    Compare the received signature with the expected one using a constant‑time
    comparison to avoid timing attacks.
    """
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        return False
    # Normalize both signatures to bytes for comparison
    try:
        expected_bytes = bytes.fromhex(expected_sig)
        received_bytes = bytes.fromhex(received_sig)
    except ValueError:
        # If the signatures are not valid hex, treat as invalid
        return False

    return hmac.compare_digest(expected_bytes, received_bytes)


def retrieve_user_info(uid: str, sig: str) -> Optional[dict]:
    """
    Fetch a user profile from the remote system and verify its authenticity.

    Parameters
    ----------
    uid : str
        The unique identifier of the user.
    sig : str
        The cryptographic signature that accompanies the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the remote system cannot be reached or a network error occurs.
    """
    # First, verify that we have an expected signature for this user
    if not _verify_signature(uid, sig):
        return None

    try:
        response = requests.get(
            USER_PROFILE_ENDPOINT.format(uid=uid),
            timeout=5,  # seconds
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Any connectivity or HTTP error results in a ConnectionError
        raise ConnectionError(f"Unable to fetch profile for user {uid}") from exc

    try:
        profile = response.json()
    except ValueError as exc:
        # Response was not valid JSON; treat as a connectivity issue
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    # The signature was already validated against the expected value,
    # so we can safely return the profile.
    return profile