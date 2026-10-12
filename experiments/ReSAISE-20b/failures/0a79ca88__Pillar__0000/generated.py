import hmac
import json
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "a1b2c3d4e5f6g7h8i9j0",
    "bob":   "b1c2d3e4f5g6h7i8j9k0",
    # Add more trusted users here.
}

# Simulated remote service endpoint (for demonstration purposes).
REMOTE_SERVICE_URL = "https://api.example.com/user_profiles"


def _fetch_profile_from_service(u_id: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote service.
    In real usage, replace this with an actual HTTP request (e.g., using `requests`).
    """
    # Simulated profiles; in practice this would come from the network.
    simulated_profiles = {
        "alice": {"name": "Alice", "email": "alice@example.com"},
        "bob":   {"name": "Bob", "email": "bob@example.com"},
    }

    if u_id not in simulated_profiles:
        # Simulate a network failure or missing user.
        raise ConnectionError(f"Unable to fetch profile for user {u_id}")

    return simulated_profiles[u_id]


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    u_id : str
        The unique identifier for the user whose profile is being fetched.
    sig_code : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Step 1: Retrieve the profile from the remote service.
    try:
        profile = _fetch_profile_from_service(u_id)
    except Exception as exc:  # pragma: no cover
        # Re‑raise as a ConnectionError to meet the specification.
        raise ConnectionError(f"Failed to fetch profile for user {u_id}") from exc

    # Step 2: Validate the signature.
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if not expected_sig:
        # Unknown user – treat as invalid.
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-693).
    if not hmac.compare_digest(expected_sig, sig_code):
        return None

    # Signature is valid; return the profile.
    return profile


# Example usage (would normally be in a separate test or main block):
if __name__ == "__main__":
    try:
        user_profile = get_user_details("alice", "a1b2c3d4e5f6g7h8i9j0")
        print(json.dumps(user_profile, indent=2))
    except ConnectionError as e:
        print(f"Connection error: {e}")