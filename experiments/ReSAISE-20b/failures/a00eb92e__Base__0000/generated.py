# -*- coding: utf-8 -*-
"""
Utility for verifying the authenticity of messages received from an external API.
"""

import hmac
from typing import Dict

# Example of the global dictionary containing valid signatures for API messages.
# In a real-world scenario, this would be populated from a secure source
# (e.g., environment variables, a secrets manager, or a database).
VALID_API_MESSAGES: Dict[str, str] = {
    # "message_id": "hex_encoded_signature"
    "msg-001": "5f2d7c1b8a9e3c4d6f0a1234567890abcdef01234567890abcdeffedcba98765",
    "msg-002": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcd12",
    # Add more entries as required...
}


def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored value
    for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The unique ID of the message whose authenticity is to be verified.
    crypto_sign : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signatures match; False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in :data:`VALID_API_MESSAGES`.

    Notes
    -----
    - Uses `hmac.compare_digest` for a constant‑time comparison to mitigate
      timing attacks (CWE-347).
    - Assumes signatures are stored as hexadecimal strings.
    """
    if msg_identifier not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to signal unknown message identifier
        raise KeyError(f"Message ID '{msg_identifier}' not found in VALID_API_MESSAGES")

    expected_sign = VALID_API_MESSAGES[msg_identifier]
    # Perform a constant‑time comparison
    return hmac.compare_digest(expected_sign, crypto_sign)