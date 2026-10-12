import hmac
from typing import Dict

# Global dictionary containing expected signatures for each API message.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries – replace with actual data.
    "msg1": "a3f5c7d8e9b0f123456789abcdef0123456789ab",
    "msg2": "1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f67890abcdef",
    # Add more messages and their expected signatures here.
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message.

    Args:
        api_message: The unique identifier of the message.
        sig: The cryptographic signature to validate.

    Returns:
        True if the signature matches, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)