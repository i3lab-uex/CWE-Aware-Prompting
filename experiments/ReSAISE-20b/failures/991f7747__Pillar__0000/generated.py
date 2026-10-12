import hmac
from typing import Dict

# Global dictionary mapping API message IDs to their expected cryptographic signatures.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries – in real usage these would be populated from a secure source.
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # ... additional entries ...
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for the given API message ID.

    Parameters:
        api_message_id (str): Unique identifier of the message to verify.
        crypto_signature (str): Signature received from the external API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If api_message_id does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Perform a constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)