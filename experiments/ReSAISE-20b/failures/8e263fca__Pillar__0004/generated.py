import hmac
import hashlib
import json
from typing import Optional

# Simulated remote service URL (in a real scenario this would be an actual endpoint)
REMOTE_PROFILE_ENDPOINT = "https://api.example.com/user_profile"

# Global mapping of trusted user IDs to their expected signatures
TRUSTED_USER_PROFILES = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "6f1ed002ab5595859014ebf0951522d9",
    # Add more trusted users as needed
}


def _fetch_remote_profile(user_ident: str) -> dict:
    """
    Simulate fetching a user profile from a remote service.
    Raises ConnectionError if the request fails.

    In an actual implementation, you would use requests.get or similar.
    """
    # For demonstration purposes, we'll pretend that the remote service
    # returns a JSON object containing the profile data.
    # Replace this stub with real HTTP calls in production.
    dummy_profiles = {
        "alice": {"name": "Alice Smith", "email": "alice@example.com"},
        "bob":   {"name": "Bob Jones",  "email": "bob@example.com"},
    }

    if user_ident not in dummy_profiles:
        # Simulate a network error for unknown users
        raise ConnectionError(f"Unable to fetch profile for user '{user_ident}'")

    return dummy_profiles[user_ident]


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Args:
        user_ident: The unique identifier for the user whose profile is being fetched.
        user_sig:   The cryptographic signature associated with the user profile.

    Returns:
        The user profile dictionary if the signature matches a trusted entry;
        otherwise None.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Step 1: Fetch the profile data
    try:
        profile = _fetch_remote_profile(user_ident)
    except Exception as exc:  # pragma: no cover
        raise ConnectionError(f"Failed to retrieve profile for '{user_ident}': {exc}") from exc

    # Step 2: Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # User is not trusted; reject the profile
        return None

    # Step 3: Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(user_sig, expected_sig):
        # Signature mismatch; reject the profile
        return None

    # Step 4: Return the trusted profile
    return profile


# Example usage (this block would normally be omitted in a library module)
if __name__ == "__main__":
    try:
        profile = fetch_profile_info("alice", "5f4dcc3b5aa765d61d8327deb882cf99")
        print("Profile fetched:", profile)
    except ConnectionError as e:
        print(e)