import hmac
from typing import Dict

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# In a real application this would be populated securely from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}

def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Args:
        api_message_id (str): Unique identifier of the message.
        crypto_signature (str): Signature to validate.

    Returns:
        bool: True if the signature is valid for the message ID, False otherwise.

    Raises:
        KeyError: If the api_message_id is not present in VALID_API_MESSAGES.
    """
    # Retrieve expected signature; raise KeyError if ID is missing
    try:
        expected_signature = VALID_API_MESSAGES[api_message_id]
    except KeyError as exc:
        raise KeyError(f"API message ID '{api_message_id}' not found.") from exc

    # Use constant‑time comparison to prevent timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)