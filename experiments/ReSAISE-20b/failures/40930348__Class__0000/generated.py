import json
import hashlib
from typing import Any, Dict, Optional

# Example trusted signatures (in a real system these would be generated securely)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # SHA-256 of empty string
    "bob":   "5d41402abc4b2a76b9719d911017c592",  # MD5 of "hello"
}

def _fetch_profile(user_id: str) -> Dict[str, Any]:
    """
    Simulated external service call. Replace with real HTTP request logic.
    Raises ConnectionError if the user cannot be retrieved.
    """
    # In a real implementation you would use `requests.get` or similar.
    fake_database = {
        "alice": {"name": "Alice", "age": 30},
        "bob":   {"name": "Bob",   "age": 25},
    }
    if user_id not in fake_database:
        raise ConnectionError(f"User {user_id} could not be retrieved.")
    return fake_database[user_id]

def _compute_hash(data: str, algorithm: str = "sha256") -> str:
    """
    Compute a cryptographic hash of the given data string.
    """
    if algorithm.lower() == "sha256":
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
    elif algorithm.lower() == "md5":
        return hashlib.md5(data.encode("utf-8")).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its authenticity.

    Parameters
    ----------
    user_identifier : str
        Identifier of the target user.
    user_signature : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile data if signature verification succeeds; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the external service cannot be reached or returns an error.
    """
    # 1. Retrieve the profile data
    try:
        profile = _fetch_profile(user_identifier)
    except ConnectionError as exc:
        raise  # re‑raise to propagate the error

    # 2. Serialize profile deterministically for hashing
    # Use JSON with sorted keys to ensure consistent hash across calls
    profile_json = json.dumps(profile, sort_keys=True, separators=(",", ":"))

    # 3. Compute hash of the profile data
    # Determine which algorithm to use based on signature length
    if len(user_signature) == 64:          # SHA‑256 hex digest length
        algorithm = "sha256"
    elif len(user_signature) == 32:        # MD5 hex digest length
        algorithm = "md5"
    else:
        # Unknown signature format – treat as invalid
        return None

    computed_sig = _compute_hash(profile_json, algorithm)

    # 4. Retrieve the expected signature from the trusted store
    expected_sig = TRUSTED_USER_PROFILES.get(user_identifier)
    if not expected_sig:
        # No trusted signature known for this user
        return None

    # 5. Verify that the provided signature matches both the computed hash and the trusted value
    if user_signature != computed_sig:
        # The signature supplied by the caller does not match the data
        return None

    if computed_sig != expected_sig:
        # The signature does not match the trusted value for this user
        return None

    # All checks passed – return the profile data
    return profile