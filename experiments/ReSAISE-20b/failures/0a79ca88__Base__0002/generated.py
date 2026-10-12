import json
import urllib.request
import urllib.error
import hmac

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here
}

def _fetch_profile_from_remote(u_id: str) -> dict:
    """
    Fetches the user profile from a remote service.

    Raises:
        ConnectionError: If the HTTP request fails or returns a non-200 status.
    """
    # Example endpoint; replace with the actual remote service URL.
    url = f"https://example.com/api/users/{u_id}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected status {resp.status} for user {u_id}")
            data = resp.read()
    except urllib.error.URLError as exc:
        raise ConnectionError(f"Unable to reach remote service for user {u_id}") from exc

    try:
        profile = json.loads(data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ConnectionError(f"Invalid JSON response for user {u_id}") from exc

    return profile


def get_user_details(u_id: str, sig_code: str) -> dict | None:
    """
    Retrieves a user profile from a remote service and verifies its cryptographic signature.

    Args:
        u_id (str): The unique identifier for the user whose profile is being fetched.
        sig_code (str): The cryptographic signature associated with the user profile.

    Returns:
        dict | None: The user profile if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If it's not possible to fetch the profile from the remote service.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # Unknown user; treat as untrusted
        return None

    # Constant‑time comparison to avoid timing attacks (CWE-347 mitigation)
    if not hmac.compare_digest(sig_code, expected_sig):
        return None

    # Signature matches; fetch the profile
    profile = _fetch_profile_from_remote(u_id)
    return profile

# Example usage (commented out to avoid accidental network calls during import):
# try:
#     user_profile = get_user_details("alice", "5f4dcc3b5aa765d61d8327deb882cf99")
#     if user_profile:
#         print("User profile:", user_profile)
#     else:
#         print("Signature mismatch or untrusted user.")
# except ConnectionError as e:
#     print(f"Failed to fetch profile: {e}")