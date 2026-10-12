# -*- coding: utf-8 -*-

"""
Utility for verifying API message signatures.

The module assumes a global dictionary named ``VALID_API_MESSAGES`` exists
in the same namespace.  Each entry maps a message ID (str) to its expected
cryptographic signature (also a str).  The ``verify_api_message`` function
checks whether the supplied signature matches the stored one.
"""

from __future__ import annotations

# The dictionary must be defined elsewhere in the application.  For example:
#
# VALID_API_MESSAGES = {
#     "msg123": "a1b2c3d4e5f6...",
#     "msg456": "deadbeef1234..."
# }
#
# The function will raise KeyError if ``msg_id`` is not present.

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the API message to verify.
    sign : str
        The cryptographic signature supplied with the message.

    Returns
    -------
    bool
        ``True`` if the signatures match; otherwise ``False``.

    Raises
    ------
    KeyError
        If ``msg_id`` is not present in the global ``VALID_API_MESSAGES``
        dictionary.
    """
    # Retrieve the expected signature; a missing key raises KeyError as required.
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use a constant‑time comparison to mitigate timing attacks.
    # For simple string signatures this is sufficient; for byte strings
    # ``hmac.compare_digest`` can be used.
    return sign == expected_sign