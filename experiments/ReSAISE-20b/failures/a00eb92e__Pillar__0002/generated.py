import hmac

# Global dictionary mapping message identifiers to their expected cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries; in production these would be populated from a secure source.
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "6b1b36cbb04bd280a9a76d61e0f7d1c4",
    # ... more entries ...
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters:
        msg_identifier (str): The unique ID of the API message.
        crypto_sign (str): The cryptographic signature received from the external API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if identifier is unknown
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(expected_sign, crypto_sign)

# Example usage (for testing purposes only; remove or guard in production)
if __name__ == "__main__":
    try:
        result = check_message_authenticity("msg-001", "5f4dcc3b5aa765d61d8327deb882cf99")
        print(f"Authenticity check passed: {result}")
    except KeyError as e:
        print(f"Message ID not found: {e}")