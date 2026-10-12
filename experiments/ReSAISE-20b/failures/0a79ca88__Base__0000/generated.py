import hmac
import json
from typing import Any, Dict, Optional

# Global mapping of trusted user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real data in production
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "1234567890abcdef1234",
}

# Simulated remote service endpoint (replace with the real URL in production)
REMOTE_SERVICE_URL = "https://api.example.com/user_profiles/"

def _fetch_profile_from_remote(u_id: str) -> Dict[str, Any]:
    """
    Fetch the user profile from a remote service.
    In a real implementation this would perform an HTTP GET request
    and parse the JSON response. Here we raise a ConnectionError
    to mimic a failure scenario.
    """
    # TODO: Replace with actual network call, e.g.:
    #   response = requests.get(f"{REMOTE_SERVICE_URL}{u_id}", timeout=5)
    #   response.raise_for_status()
    #   return response.json()

    raise ConnectionError(f"Unable to fetch profile for user {u_id}")

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote service and verify its
    cryptographic signature against the trusted list.

    Parameters:
        u_id (str): The unique identifier of the user.
        sig_code (str): The cryptographic signature provided for the profile.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match or the user ID is unknown.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # 1. Fetch the profile data
    try:
        profile = _fetch_profile_from_remote(u_id)
    except Exception as exc:
        # Wrap any exception from the remote call into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {u_id}") from exc

    # 2. Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if not expected_sig:
        # Unknown user – treat as untrusted
        return None

    # 3. Compare signatures using a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig_code, expected_sig):
        # Signature mismatch – do not return the profile
        return None

    # 4. All checks passed – return the trusted profile
    return profile