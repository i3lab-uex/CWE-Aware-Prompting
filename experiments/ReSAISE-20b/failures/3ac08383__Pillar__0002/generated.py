import hashlib
import hmac

# Example dictionary of valid signatures for demonstration purposes.
# In a real application, this should be securely stored and managed.
VALID_API_MESSAGES = {
    "msg1": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg2": "e99a18c428cb38d5f260853678922e03",
    # Add more messages and their expected signatures here
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message.

    Args:
        api_message (str): Unique identifier of the API message.
        sig (str): Hexadecimal cryptographic signature to validate.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `api_message` does not exist in VALID_API_MESSAGES.
    """
    # Ensure the message exists; raise KeyError if not found
    expected_sig = VALID_API_MESSAGES[api_message]

    # Convert signatures to bytes for comparison
    expected_bytes = bytes.fromhex(expected_sig)
    provided_bytes = bytes.fromhex(sig)

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_bytes, provided_bytes)