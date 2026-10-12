import requests
import hmac

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES = {
    "alice": "d2c9e6f1b4a3a8c7d5e0f8c2b9a6f1e4",
    "bob":   "3f5d8c2b7a9e1f0d4c6b8a3e5f7d2c1",
    # Add more trusted user signatures here.
}

def fetch_profile_info(user_ident: str, user_sig: str):
    """
    Fetch a user profile from a remote service and verify its cryptographic signature.

    Args:
        user_ident (str): The unique identifier for the user whose profile is being fetched.
        user_sig (str): The cryptographic signature associated with the user profile.

    Returns:
        dict | None: The user profile data if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the remote service cannot be reached or returns a non‑200 status.
    """
    # 1. Validate input types
    if not isinstance(user_ident, str) or not isinstance(user_sig, str):
        raise TypeError("user_ident and user_sig must be strings")

    # 2. Ensure the user is known
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # Unknown user – no signature to compare against
        return None

    # 3. Fetch the profile from a remote service
    try:
        response = requests.get(
            f"https://api.example.com/users/{user_ident}",
            timeout=5  # seconds
        )
    except requests.RequestException as exc:
        raise ConnectionError("Failed to connect to the remote service") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Remote service returned unexpected status {response.status_code}"
        )

    try:
        profile = response.json()
    except ValueError as exc:
        raise ConnectionError("Failed to parse JSON from remote service") from exc

    # 4. Verify the signature using constant‑time comparison
    if not hmac.compare_digest(user_sig, expected_sig):
        # Signature mismatch – treat as untrusted
        return None

    # 5. Return the verified profile
    return profile