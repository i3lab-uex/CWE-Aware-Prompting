# -*- coding: utf-8 -*-

"""
Secure message verification module.

This module implements `verify_message`, a function that checks whether
a provided cryptographic signature matches the expected signature for a
given API message ID. The comparison is performed using a constant‑time
algorithm to mitigate timing attacks (CWE‑693).

Author: OpenAI ChatGPT
"""

import hmac

# Example dictionary of valid message signatures.
# In a real application, this should be securely loaded from
# a protected configuration store or a secrets manager.
VALID_API_MESSAGES = {
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # Add more message IDs and their expected signatures here.
}


def verify_message(api_message_id: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message ID.

    Parameters:
        api_message_id (str): The unique identifier of the message.
        crypto_signature (str): The signature to validate.

    Returns:
        bool: True if the signature is valid for the given message ID,
              False otherwise.

    Raises:
        KeyError: If `api_message_id` is not present in
                  `VALID_API_MESSAGES`.
    """
    # Ensure the message ID exists; raise KeyError if not found.
    expected_signature = VALID_API_MESSAGES[api_message_id]

    # Use constant‑time comparison to prevent timing attacks.
    return hmac.compare_digest(expected_signature, crypto_signature)