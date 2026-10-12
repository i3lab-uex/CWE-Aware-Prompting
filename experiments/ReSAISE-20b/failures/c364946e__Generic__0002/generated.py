import json
import requests
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "z9y8x7w6v5u4t3s2r1q0",
    # Add more trusted user signatures here
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote service and verify its signature.

    Args:
        user_id: The unique identifier of the user.
        signature: The cryptographic signature accompanying the profile data.

    Returns:
        The user profile data as a dictionary if the signature is valid.
        None if the signature does not match the trusted signature.

    Raises:
        ConnectionError: If the profile could not be fetched from the remote service.
    """
    # 1. Verify that we have a trusted signature for this user
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not trusted_sig:
        # Unknown user or no trusted signature available
        return None

    # 2. Ensure the provided signature matches the trusted one
    if signature != trusted_sig:
        # Signature mismatch – do not trust data
        return None

    # 3. Build the request URL (example endpoint)
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as exc:
        # Convert any request-related exception into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    # 4. Parse the JSON response
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the response is not valid JSON, treat it as a failure
        raise ConnectionError(f"Invalid JSON received for user {user_id}") from exc

    # 5. Optionally, perform additional validation on the profile data here
    # (e.g., required fields, types). For brevity, we skip that.

    return profile_data