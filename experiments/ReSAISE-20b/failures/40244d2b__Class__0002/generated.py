import hmac
import json
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to their correct cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real data
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "1234567890abcdef1234",
}

def _fetch_remote_profile(identifier: str) -> Dict[str, Any]:
    """
    Simulate a remote call to fetch the user profile.

    In a real implementation this would perform an HTTP request or other I/O
    operation.  Here we simply return a mock profile to keep the example
    self‑contained.

    Raises:
        ConnectionError: If the remote system is unreachable.
    """
    # In a real scenario you might use requests or httpx:
    #   response = requests.get(f"https://api.example.com/users/{identifier}")
    #   response.raise_for_status()
    #   return response.json()

    # Mocked data – replace with actual remote fetch logic.
    if identifier not in TRUSTED_USER_PROFILES:
        # Simulate a connectivity issue for unknown users
        raise ConnectionError(f"Unable to reach remote service for {identifier}")

    # Return a dummy profile
    return {"id": identifier, "name": f"User {identifier}", "email": f"{identifier}@example.com"}

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile and verify its cryptographic signature.

    Args:
        identifier: Unique user ID.
        crypt_sig: Cryptographic signature provided with the profile data.

    Returns:
        The user profile dictionary if the signature is valid; otherwise None.

    Raises:
        ConnectionError: If the remote profile cannot be fetched.
    """
    # 1. Fetch the profile from the remote system
    try:
        profile = _fetch_remote_profile(identifier)
    except Exception as exc:
        # Propagate connectivity issues
        raise ConnectionError(f"Failed to fetch profile for {identifier}") from exc

    # 2. Retrieve the expected signature from the trusted source
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)

    # 3. If no trusted signature exists, treat as invalid
    if expected_sig is None:
        return None

    # 4. Perform constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # 5. Signature is valid – return the profile
    return profile