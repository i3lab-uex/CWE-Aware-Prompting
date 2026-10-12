import hmac
from typing import Dict

# Global dictionary mapping API message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries; replace with actual values in production.
    "msg_001": "a3f5c8e2b1d9...",
    "msg_002": "4d7e9f3a0b1c...",
    # ...
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature `sig` matches the expected
    signature for the given `api_message`.

    Args:
        api_message: Unique identifier of the API message.
        sig: Cryptographic signature to validate.

    Returns:
        True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message exists; raise KeyError if it does not.
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to prevent timing attacks.
    return hmac.compare_digest(expected_sig, sig)