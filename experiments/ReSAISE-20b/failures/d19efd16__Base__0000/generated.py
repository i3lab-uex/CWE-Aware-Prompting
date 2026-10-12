import json
import hashlib
import hmac
from typing import Any, Dict, Optional

# Example global dictionary of trusted signatures.
# In a real system this would be populated from a secure source.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # "user_id": "<hex digest of the signed payload>"
}

def _fetch_profile_from_service(profile_id: str) -> Dict[str, Any]:
    """
    Simulated external service call. Replace with actual API logic.
    Raises ConnectionError if the request fails.
    """
    # Placeholder for real HTTP request
    # For example:
    # response = requests.get(f"https://api.example.com/profiles/{profile_id}", timeout=5)
    # response.raise_for_status()
    # return response.json()

    # Simulated data for demonstration purposes
    simulated_profiles = {
        "alice": {"name": "Alice", "age": 30},
        "bob": {"name": "Bob", "age": 25},
    }
    if profile_id not in simulated_profiles:
        raise ConnectionError(f"Profile {profile_id} not found")
    return simulated_profiles[profile_id]


def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile and validate its cryptographic signature.

    Args:
        profile_id: Identifier of the user profile to fetch.
        profile_sig: Cryptographic signature (hex string) provided with the payload.

    Returns:
        The user profile dictionary if the signature is valid and matches the
        trusted signature; otherwise, None.

    Raises:
        ConnectionError: If the profile cannot be retrieved from the external service.
    """
    try:
        # Step 1: Retrieve profile data from external source
        profile_data = _fetch_profile_from_service(profile_id)
    except Exception as exc:
        # Any failure in fetching is treated as a connection error
        raise ConnectionError(f"Failed to retrieve profile {profile_id}") from exc

    # Step 2: Canonicalize JSON for deterministic hashing
    profile_json = json.dumps(profile_data, separators=(",", ":"), sort_keys=True)

    # Step 3: Compute SHA-256 digest of the canonical JSON
    computed_digest = hashlib.sha256(profile_json.encode("utf-8")).hexdigest()

    # Step 4: Verify that the provided signature matches both the computed digest
    # and the trusted signature stored in TRUSTED_USER_PROFILES.
    expected_trusted_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_trusted_sig:
        # No trusted signature available for this profile
        return None

    # Constant-time comparison to avoid timing attacks
    if hmac.compare_digest(computed_digest, profile_sig) and \
       hmac.compare_digest(computed_digest, expected_trusted_sig):
        return profile_data

    # Signature mismatch
    return None