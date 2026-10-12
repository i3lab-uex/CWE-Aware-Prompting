import hmac
import hashlib
from typing import Dict, Any, Optional

# Global mapping of user IDs to their expected cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f67890",
    "alice456": "0fedcba987654321",
    # Add more trusted user IDs and signatures as needed
}


def _fetch_remote_profile(u_id: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote service.
    In a real implementation this would perform an HTTP request or
    another network operation. Here we simply return a stubbed profile.
    
    Raises:
        ConnectionError: If the remote service is unreachable or returns an error.
    """
    # For demonstration, pretend that fetching fails for a specific ID
    if u_id == "unreachable":
        raise ConnectionError(f"Unable to reach remote service for user {u_id}")

    # Stubbed profile data
    return {
        "user_id": u_id,
        "name": "John Doe",
        "email": f"{u_id}@example.com",
    }


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Args:
        u_id (str): Unique identifier for the user.
        sig_code (str): Cryptographic signature associated with the user profile.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Fetch profile from remote service
    try:
        profile = _fetch_remote_profile(u_id)
    except Exception as exc:  # Catch broad exception to re‑raise as ConnectionError
        raise ConnectionError(f"Failed to fetch profile for {u_id}") from exc

    # Retrieve expected signature
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # Unknown user ID: treat as untrusted
        return None

    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig_code, expected_sig):
        return None

    # Signature matches; profile is considered trustworthy
    return profile