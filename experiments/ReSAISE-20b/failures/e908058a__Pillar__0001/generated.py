import json
import requests
from typing import Optional

# Example global dictionary mapping user IDs to their correct signatures.
TRUSTED_USER_PROFILES = {
    "user-123": "abcd1234efgh5678",
    # ... other entries
}

def collect_user_data(uuid: str, sig_hash: str) -> Optional[dict]:
    """
    Fetches a user profile from the remote system and verifies its signature.

    Args:
        uuid (str): The unique identifier for the user.
        sig_hash (str): The cryptographic signature provided with the profile data.

    Returns:
        Optional[dict]: The user profile data if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If the profile cannot be fetched due to connectivity issues.
    """
    # URL construction – keep it simple and avoid user input in the path
    url = f"https://api.example.com/users/{uuid}/profile"

    try:
        # Use a short timeout and verify SSL certificates
        response = requests.get(url, timeout=5.0, verify=True)
    except (requests.ConnectionError, requests.Timeout) as exc:
        # Wrap lower‑level exceptions in a ConnectionError to match the spec
        raise ConnectionError(f"Failed to connect to {url}") from exc

    if response.status_code != 200:
        # Non‑successful HTTP status – treat as connectivity failure
        raise ConnectionError(f"Unexpected status {response.status_code} for {url}")

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # Malformed JSON – treat as a connectivity/format issue
        raise ConnectionError(f"Invalid JSON response from {url}") from exc

    # Verify the signature against the trusted mapping
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not expected_sig or sig_hash != expected_sig:
        return None

    # All checks passed; return the profile data
    return profile_data