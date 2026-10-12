import requests
from typing import Dict, Any, Optional

# Global mapping of user IDs to the expected cryptographic signatures for their profiles
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real data in production
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "z9y8x7w6v5u4t3s2r1q0",
    # Add more trusted user IDs and their signatures here
}

def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service after validating its cryptographic signature.

    Parameters
    ----------
    profile_id : str
        Identifier of the user whose profile is to be fetched.
    profile_sig : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    Optional[Dict[str, Any]]
        The user profile data if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If the profile could not be retrieved from the external service.
    """
    # 1. Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_sig:
        # Unknown user – cannot trust the signature
        return None

    # 2. Compare the provided signature with the expected one
    if profile_sig != expected_sig:
        # Signature mismatch – do not trust the data
        return None

    # 3. Retrieve the profile from an external service
    url = f"https://api.example.com/profiles/{profile_id}"
    try:
        response = requests.get(url, timeout=5.0, verify=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Wrap any request-related error into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for '{profile_id}': {exc}") from exc

    # 4. Return the JSON-decoded profile data
    try:
        return response.json()
    except ValueError as exc:
        # Response was not valid JSON – treat it as a retrieval failure
        raise ConnectionError(f"Invalid JSON response for profile '{profile_id}': {exc}") from exc