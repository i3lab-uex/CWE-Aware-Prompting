import requests
import hmac

# Global mapping of user IDs to the correct cryptographic signature.
TRUSTED_USER_PROFILES = {
    "user1": "a1b2c3d4e5f6g7h8i9j0",
    "user2": "abcdef1234567890abcd",
    # Add more user IDs and signatures as needed.
}

def _fetch_profile(identifier: str) -> dict:
    """
    Simulates fetching a user profile from a remote system.
    Replace this with the actual API call in production.
    """
    # Example URL – replace with real endpoint
    url = f"https://api.example.com/users/{identifier}"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def access_user_details(identifier: str, crypt_sig: str) -> dict | None:
    """
    Retrieve a user profile and verify its cryptographic signature.

    Args:
        identifier: The unique identifier for the user.
        crypt_sig:   The signature provided with the profile data.

    Returns:
        dict or None – The user profile if the signature is valid,
        otherwise None.

    Raises:
        ConnectionError: If there was a problem connecting to the remote system.
    """
    try:
        profile = _fetch_profile(identifier)
    except requests.RequestException as exc:
        # Convert any request-related exception to a ConnectionError
        raise ConnectionError("Unable to fetch user profile.") from exc

    # Retrieve the expected signature for this identifier
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if not expected_sig:
        # No trusted signature known – treat as invalid
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑347)
    if hmac.compare_digest(crypt_sig, expected_sig):
        return profile
    return None