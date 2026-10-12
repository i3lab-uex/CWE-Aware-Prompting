import requests
from hashlib import sha256
from hmac import compare_digest

# Global mapping of user IDs to their trusted signature hashes (hex strings)
TRUSTED_USER_PROFILES = {
    # Example entries – replace with real data
    "user-123": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd7c8e7b1f2c5b9e8d3",
    "user-456": "6cf615d4f5a0c2b3e8d9f7b1a6c9e4b2d0f3a5c8e9b7d1a6f2c4e3b0d1a5c8e9",
    # ...
}

def collect_user_data(uuid: str, sig_hash: str):
    """
    Fetch a user profile from the remote service and verify its signature.

    Parameters
    ----------
    uuid : str
        Unique identifier of the user.
    sig_hash : str
        Hexadecimal representation of the cryptographic signature supplied with the profile.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or service error.
    """
    # Step 1: Retrieve the trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not expected_sig:
        # No trusted signature known for this user – treat as invalid
        return None

    # Step 2: Fetch the profile data from the remote system
    try:
        response = requests.get(
            f"https://api.example.com/users/{uuid}",
            timeout=5.0,  # seconds
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any request-related exception into a ConnectionError
        raise ConnectionError(f"Unable to fetch user profile for {uuid}") from exc

    # Step 3: Verify the supplied signature matches the expected one
    # Use constant‑time comparison to mitigate timing attacks.
    if not compare_digest(sig_hash.lower(), expected_sig.lower()):
        return None

    # Step 4: Return the profile data (JSON decoded)
    try:
        return response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid response format for user {uuid}") from exc