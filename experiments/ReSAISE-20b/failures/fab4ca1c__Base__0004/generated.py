import hmac
from typing import Dict

# Example dictionary of valid signatures for demonstration purposes.
# In a real application this would be populated securely from
# the external API or a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    # msg_identifier : hex-encoded signature
    "msg1": "a3f4c2d9b8e7f6... (hex signature)",
    "msg2": "4c1b9a8d7e6f5... (hex signature)",
    # Add additional message identifiers and their signatures here
}


def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the
    expected signature for a given message identifier.

    Parameters:
        msg_identifier (str): Identifier of the message to verify.
        sign (str): Hex-encoded cryptographic signature provided by
                    the external API.

    Returns:
        bool: True if the signature matches, False otherwise.

    Raises:
        KeyError: If `msg_identifier` is not present in
                  VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use hmac.compare_digest for a timing‑attack resistant comparison
    return hmac.compare_digest(sign.lower(), expected_sign.lower())