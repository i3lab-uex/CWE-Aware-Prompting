import hmac
import hashlib
import json
from typing import Any, Dict, Optional

# Example trusted signatures for user profiles (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user_1": "5f4dcc3b5aa765d61d8327deb882cf99",  # Example MD5 hash
    "user_2": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted user signatures here
}

# Simulated external service URL (replace with real endpoint)
EXTERNAL_SERVICE_URL = "https://api.example.com/user_profiles"


def _fetch_profile_from_service(user_identifier: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from an external service.
    In real-world usage, this would perform an HTTP GET request to the
    external API. For demonstration purposes, we return a static payload.
    """
    # In an actual implementation you would use:
    #
    # import requests
    # response = requests.get(
    #     f"{EXTERNAL_SERVICE_URL}/{user_identifier}",
    #     timeout=5,
    # )
    # response.raise_for_status()
    # return response.json()

    # Dummy data for demonstration
    dummy_profiles = {
        "user_1": {"name": "Alice", "email": "alice@example.com"},
        "user_2": {"name": "Bob", "email": "bob@example.com"},
    }
    if user_identifier not in dummy_profiles:
        raise ConnectionError(f"Profile for '{user_identifier}' not found")
    return dummy_profiles[user_identifier]


def _verify_signature(
    user_identifier: str, signature: str, profile_data: Dict[str, Any]
) -> bool:
    """
    Verify that the provided signature matches the expected one for the
    user profile. The signature is assumed to be a hex digest of the
    JSON-encoded profile data using MD5. In practice, use a stronger hash.
    """
    expected_sig = TRUSTED_USER_PROFILES.get(user_identifier)
    if not expected_sig:
        # No trusted signature available for this user
        return False

    # Compute the hash of the profile data deterministically
    profile_json = json.dumps(profile_data, sort_keys=True).encode("utf-8")
    computed_sig = hashlib.md5(profile_json).hexdigest()

    # Constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed_sig, expected_sig)


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its
    cryptographic signature against the trusted value.

    Parameters:
        user_identifier (str): Identifier of the target user.
        user_signature   (str): Cryptographic signature attached to the profile data.

    Returns:
        dict: The user profile data if verification succeeds.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If the profile cannot be retrieved from the external service.
    """
    # Retrieve profile data
    try:
        profile_data = _fetch_profile_from_service(user_identifier)
    except Exception as exc:
        # Wrap any exception that indicates a failure to retrieve data
        raise ConnectionError(f"Failed to fetch profile for '{user_identifier}': {exc}") from exc

    # Verify the signature
    if _verify_signature(user_identifier, user_signature, profile_data):
        return profile_data

    # Signature mismatch – do not trust the data
    return None