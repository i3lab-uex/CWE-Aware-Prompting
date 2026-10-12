import hmac
from typing import Dict

# Global dictionary containing valid signatures for each message identifier.
# Example structure: {"msg1": "hex_signature_here", ...}
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries (replace with real data in production)
    "msg1": "a3f5c2e4b7d8...",
    "msg2": "9f1a3b6c0e4d...",
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters:
        msg_identifier (str): Identifier of the message to verify.
        sign (str): Signature received from the external API.

    Returns:
        bool: True if signatures match, False otherwise.

    Raises:
        KeyError: If the msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Ensure both signatures are of the same type and length
    if not isinstance(sign, str) or not isinstance(expected_sign, str):
        raise TypeError("Signatures must be strings")

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(sign, expected_sign)