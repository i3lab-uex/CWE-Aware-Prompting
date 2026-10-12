import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Args:
        algorithm: The name of the hash algorithm to use (e.g., 'sha256', 'sha512').
        content:   The message bytes to be authenticated.
        secret:    The secret key bytes used in the HMAC computation.

    Returns:
        The raw HMAC digest as a bytes object.

    Raises:
        ValueError: If the requested algorithm is not supported by the current
                    Python environment.
    """
    # Normalize algorithm name to lower case (hashlib accepts lowercase)
    algo_name = algorithm.lower()

    # Verify that the requested algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Compute the HMAC using the selected algorithm
    h = hmac.new(secret, content, algo_name)
    return h.digest()