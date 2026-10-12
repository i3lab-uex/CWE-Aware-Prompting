# -*- coding: utf-8 -*-
"""
Utility to authenticate messages received from an external API.

The module relies on a global dictionary `VALID_API_MESSAGES` that maps
message identifiers to the expected cryptographic signature strings.
"""

import hmac
from typing import Dict

# Example placeholder for the global dictionary.
# In a real application this should be populated securely from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    # "message_id": "expected_signature",
    # e.g., "msg-12345": "a1b2c3d4e5f6...",
}


def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided `signature` matches the expected signature for
    the given `message_id`.

    Parameters
    ----------
    message_id : str
        Unique identifier of the message to authenticate.
    signature : str
        Cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        ``True`` if the signature is valid, otherwise ``False``.

    Raises
    ------
    KeyError
        If `message_id` is not present in ``VALID_API_MESSAGES``.
    """
    if message_id not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to indicate missing entry
        raise KeyError(f"Message ID '{message_id}' not found in VALID_API_MESSAGES")

    expected_sig = VALID_API_MESSAGES[message_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(expected_sig.encode("utf-8"), signature.encode("utf-8"))