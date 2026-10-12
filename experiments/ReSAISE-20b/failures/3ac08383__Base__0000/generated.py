import hmac
from typing import Dict

# Global dictionary mapping API message identifiers to their expected signatures.
# In a real application these would be securely stored and protected
# (e.g., in an HSM or encrypted config). Here we provide a placeholder.
VALID_API_MESSAGES: Dict[str, str] = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # ... more entries ...
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the supplied cryptographic signature `sig` matches
    the expected signature for the given `api_message`.

    Parameters:
        api_message (str): Identifier of the API message.
        sig (str): Cryptographic signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sig, expected_sig)