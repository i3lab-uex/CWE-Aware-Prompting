import hmac
import hashlib

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Args:
        algorithm_name (str): Name of the hashing algorithm to use.
        content (bytes): The message to be signed.
        secret (bytes): The secret key used in the HMAC process.

    Returns:
        bytes: The computed HMAC signature as a byte string.

    Raises:
        ValueError: If the specified hash algorithm is not supported or unavailable.
    """
    # Validate that the requested algorithm exists in hashlib
    if algorithm_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Create the HMAC object using the specified algorithm
    try:
        hmac_obj = hmac.new(secret, msg=content, digestmod=algorithm_name.lower())
    except (TypeError, ValueError) as exc:
        # hmac.new may raise TypeError if secret or content is not bytes
        raise ValueError(f"Failed to create HMAC object: {exc}") from exc

    # Return the raw digest bytes
    return hmac_obj.digest()