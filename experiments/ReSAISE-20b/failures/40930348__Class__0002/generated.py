import hmac
import hashlib
import json
from typing import Any, Dict, Optional

# Example of trusted signatures for each user.
# In a real application this would be stored securely (e.g., in a database or HSM).
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # user_id : expected HMAC-SHA256 signature of the JSON profile
    "alice": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd5d7c1e9e8f2b4aa87",
    "bob":   "a54d88e06612d820bc3be72877c74f257b561b19a7af6e8d9a1f5db3c8c2e5a0",
    # Add more users as needed
}

# Shared secret key used to generate/verify signatures.
# In production, use a securely generated random key and store it safely.
SECRET_KEY = b"super_secret_key"


def _fetch_profile_from_service(user_identifier: str) -> str:
    """
    Simulate fetching the user profile JSON string from an external service.
    Replace this with real network code (e.g., requests.get) in production.

    Raises:
        ConnectionError: If the external service cannot be reached.
    """
    # For demonstration purposes, we'll just return a hardcoded JSON string.
    # In real code, you would perform an HTTP request and handle errors.
    profiles = {
        "alice": json.dumps({"name": "Alice", "email": "alice@example.com"}),
        "bob":   json.dumps({"name": "Bob", "email": "bob@example.com"}),
    }
    if user_identifier not in profiles:
        raise ConnectionError(f"Profile for {user_identifier} could not be retrieved.")
    return profiles[user_identifier]


def _compute_hmac(data: str) -> str:
    """
    Compute the HMAC-SHA256 of the given data string using the shared secret key.
    Returns the hexadecimal digest.
    """
    return hmac.new(SECRET_KEY, data.encode("utf-8"), hashlib.sha256).hexdigest()


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a signed user profile from an external service and validate its authenticity.

    Args:
        user_identifier: The ID of the user whose profile is requested.
        user_signature:  The HMAC-SHA256 signature supplied with the profile data.

    Returns:
        The decoded JSON profile dictionary if the signature is verified.
        None if verification fails.

    Raises:
        ConnectionError: If the profile cannot be retrieved from the external service.
    """
    # Step 1: Retrieve the raw profile data
    try:
        raw_profile = _fetch_profile_from_service(user_identifier)
    except ConnectionError as exc:
        # Propagate the connection error to the caller
        raise

    # Step 2: Verify that we have a trusted signature for this user
    expected_signature = TRUSTED_USER_PROFILES.get(user_identifier)
    if not expected_signature:
        # No trusted signature known for this user; treat as untrusted
        return None

    # Step 3: Compute the HMAC of the retrieved profile data
    computed_signature = _compute_hmac(raw_profile)

    # Step 4: Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_signature, user_signature):
        # Signature does not match; data is untrusted
        return None

    # Step 5: The signature matches – parse and return the profile data
    try:
        profile_dict = json.loads(raw_profile)
    except json.JSONDecodeError:
        # Malformed JSON – treat as untrusted
        return None

    return profile_dict


# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Compute a valid signature for Alice's profile
    alice_profile_json = _fetch_profile_from_service("alice")
    valid_signature = _compute_hmac(alice_profile_json)

    # Retrieve and verify Alice's profile
    profile = collect_user_data("alice", valid_signature)
    print(profile)  # Should output the Alice profile dictionary