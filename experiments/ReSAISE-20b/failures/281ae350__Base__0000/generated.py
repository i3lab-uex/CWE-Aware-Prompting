import hmac
from typing import Dict

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries – in real usage these would be populated securely.
    "msg-001": "a3f9c2d1e4b8f0c7e5d6a1b2c3d4e5f6",
    "msg-002": "b7a8c9d0e1f2a3b4c5d6e7f8g9h0i1j2",
    # Add more message identifiers and signatures as needed.
}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier of the message to validate.
    crypto_signature : str
        Cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signature is valid for the given message identifier,
        otherwise False.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the global VALID_API_MESSAGES.
    """
    # Ensure the identifier exists; otherwise raise KeyError as required.
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' not found.")

    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, crypto_signature)