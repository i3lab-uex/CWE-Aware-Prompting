import hmac
from typing import Any, Dict

# Global dictionary mapping user IDs to their expected signatures.
# In a real system this would be stored securely (e.g., in an HSM or vault).
TRUSTED_USER_PROFILES: Dict[str, Dict[str, Any]] = {
    # Example entry:
    # "user123": {"profile_data": {...}, "signature": "hex_encoded_signature"}
}

def retrieve_user_data(uid: str, sig: str) -> Any | None:
    """
    Retrieve a user profile only if the provided signature matches the
    trusted signature stored in TRUSTED_USER_PROFILES.

    Parameters:
        uid (str): Identifier for the targeted user.
        sig (str): Hex-encoded cryptographic signature supplied with the data.

    Returns:
        The user profile data if verification succeeds; otherwise None.

    Raises:
        ConnectionError: If the user profile cannot be retrieved (e.g., missing entry).
    """
    # Ensure inputs are strings
    if not isinstance(uid, str) or not isinstance(sig, str):
        raise TypeError("uid and sig must be strings")

    # Retrieve the trusted entry for this user
    entry = TRUSTED_USER_PROFILES.get(uid)
    if entry is None:
        # Profile not found – treat as a retrieval failure
        raise ConnectionError(f"Unable to retrieve profile for user '{uid}'")

    # Extract the expected signature
    expected_sig = entry.get("signature")
    if not isinstance(expected_sig, str):
        # Malformed entry – treat as failure
        raise ConnectionError(f"Invalid signature format for user '{uid}'")

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not trust the data
        return None

    # Return the profile data (could be a dict or any serializable object)
    return entry.get("profile_data")