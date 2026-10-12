# -*- coding: utf-8 -*-
"""
Utility to verify the authenticity of messages received from an external API.
"""

import hmac
from typing import Dict

# Example global dictionary containing valid signatures for known message IDs.
# In a real application this would be populated from secure storage or
# configuration, not hard‑coded.
VALID_API_MESSAGES: Dict[str, str] = {
    # message_id : cryptographic_signature
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # ... add more entries as needed
}


def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The ID of the message to be verified.
    crypto_sign : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in :data:`VALID_API_MESSAGES`.

    Notes
    -----
    * The comparison uses :func:`hmac.compare_digest` to guard against timing
      attacks (CWE‑347: Improper Verification of Cryptographic Signature).
    * The function does **not** perform any key or secret management; it
      assumes the signatures are pre‑computed and stored securely.
    """
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' is unknown.")

    expected_signature = VALID_API_MESSAGES[msg_identifier]
    # Use constant‑time comparison to prevent timing attacks.
    return hmac.compare_digest(expected_signature, crypto_sign)