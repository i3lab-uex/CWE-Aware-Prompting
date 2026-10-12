import hmac
import hashlib

# Example mapping of message identifiers to their expected cryptographic signatures.
# In a real application this would be securely stored and possibly rotated regularly.
VALID_API_MESSAGES = {
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message identifier.

    Parameters:
        api_message (str): Unique identifier of the external API message.
        sig (str): Cryptographic signature supplied by the caller.

    Returns:
        bool: True if the signature is valid for the given message; False otherwise.

    Raises:
        KeyError: If the api_message identifier is not present in VALID_API_MESSAGES.
    """
    # Ensure the message identifier exists
    if api_message not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown API message identifier: {api_message}")

    # Retrieve the expected signature
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use a timing‑safe comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)