import hmac
from typing import Dict

# Global dictionary containing the expected signatures for each API message.
# In a real application this would be securely loaded from a protected source.
VALID_API_MESSAGES: Dict[str, str] = {
    "msg-001": "a1b2c3d4e5f6g7h8i9j0",
    "msg-002": "1234567890abcdef1234",
    # ... additional message IDs and their signatures ...
}

def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        Identifier of the message whose authenticity is being verified.
    cryptographic_sign : str
        Cryptographic signature supplied with the message.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `api_message_id` is not present in VALID_API_MESSAGES.
    TypeError
        If either argument is not a string.

    Notes
    -----
    The comparison uses :func:`hmac.compare_digest` to avoid timing attacks,
    mitigating CWE-693 (Protection Mechanism Failure).
    """
    if not isinstance(api_message_id, str):
        raise TypeError("api_message_id must be a string")
    if not isinstance(cryptographic_sign, str):
        raise TypeError("cryptographic_sign must be a string")

    # Retrieve the expected signature; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to prevent timing attacks
    return hmac.compare_digest(expected_sign, cryptographic_sign)