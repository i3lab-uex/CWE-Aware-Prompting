# -*- coding: utf-8 -*-
"""
Utility to validate cryptographic signatures of API messages.

The module exposes a single function `validate_api_message` that checks
whether the supplied signature matches the one stored in the global
dictionary `VALID_API_MESSAGES`.  If the message ID does not exist a
`KeyError` is raised.

Security notes:
- The function performs a constant‑time comparison using `hmac.compare_digest`
  to mitigate timing attacks when comparing signatures.
- The dictionary is assumed to be populated from a secure source; the
  module itself does not modify it.
"""

from __future__ import annotations

import hmac
from typing import Dict

# Example global dictionary of message IDs to their expected signatures.
# In a real application this would be loaded from a secure configuration
# source or environment variable and should not be modified at runtime.
VALID_API_MESSAGES: Dict[str, str] = {
    "msg_001": "a3f1c2b4d5e6f7890abc123456789012",
    "msg_002": "b4d5e6f7890abc123456789012a3f1c2",
    # ... additional entries ...
}


def validate_api_message(api_message_id: str, cryptographic_sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the stored
    value for a given API message ID.

    Parameters
    ----------
    api_message_id : str
        The unique identifier of the API message.
    cryptographic_sign : str
        The cryptographic signature received alongside the message.

    Returns
    -------
    bool
        ``True`` if the signature matches the stored value, otherwise
        ``False``.

    Raises
    ------
    KeyError
        If the supplied `api_message_id` is not present in
        ``VALID_API_MESSAGES``.
    """
    # Retrieve the expected signature; KeyError will propagate if not found
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(expected_signature, cryptographic_sign)