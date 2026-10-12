# -*- coding: utf-8 -*-
"""
Utility for verifying API message signatures.
"""

import hmac
from typing import Dict

# Example dictionary of valid signatures for each API message.
# In a real system this would be populated securely, e.g. from
# environment variables or a secure vault.
VALID_API_MESSAGES: Dict[str, str] = {
    # message_id : expected_signature
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # ... more entries ...
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the
    expected signature for a given API message.

    Parameters
    ----------
    api_message : str
        Identifier of the API message being validated.
    sig : str
        The cryptographic signature to verify.

    Returns
    -------
    bool
        ``True`` if the signature matches; otherwise ``False``.

    Raises
    ------
    KeyError
        If ``api_message`` is not present in :data:`VALID_API_MESSAGES`.

    Notes
    -----
    The comparison uses ``hmac.compare_digest`` to mitigate timing attacks
    (CWE‑693: Protection Mechanism Failure).
    """
    if api_message not in VALID_API_MESSAGES:
        raise KeyError(f"API message '{api_message}' is unknown")

    expected_sig = VALID_API_MESSAGES[api_message]
    # Use constant‑time comparison to avoid leaking timing information.
    return hmac.compare_digest(sig, expected_sig)