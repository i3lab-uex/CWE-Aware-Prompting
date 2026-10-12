import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of the given content using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s', etc.).
    content : bytes
        The message to be authenticated.
    secret : bytes
        The secret key used in the HMAC calculation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by hashlib on this system.
    """
    # Normalize algorithm name for comparison
    alg_lower = algorithm.lower()

    # Verify that the requested hash algorithm is available in this environment
    if alg_lower not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Compute the HMAC using the chosen algorithm
    return hmac.new(secret, content, alg_lower).digest()