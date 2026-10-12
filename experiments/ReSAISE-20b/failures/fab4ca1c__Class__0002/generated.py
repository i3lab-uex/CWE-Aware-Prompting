import hmac
from typing import Dict

# Global dictionary containing valid signatures for each message identifier.
# Example structure: {'msg1': 'signature1', 'msg2': 'signature2'}
VALID_API_MESSAGES: Dict[str, str] = {
    # Populate with real data in production
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided signature matches the stored valid signature
    for the given message identifier.

    Args:
        msg_identifier: The unique identifier of the API message.
        sign: The cryptographic signature received from the external API.

    Returns:
        True if the signature is valid for the message identifier, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    # Ensure the identifier exists; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)