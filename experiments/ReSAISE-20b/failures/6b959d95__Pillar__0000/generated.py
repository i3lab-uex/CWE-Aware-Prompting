import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of *content* using the specified *algorithm* and *secret* key.

    Parameters
    ----------
    algorithm : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    content : bytes
        The message to be authenticated.
    secret : bytes
        The secret key for the HMAC.

    Returns
    -------
    bytes
        The raw HMAC digest value.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on this system.
    """
    # Normalize algorithm name to lower case for comparison
    algo_name = algorithm.lower()

    # Check if the algorithm is supported by hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    # Create the HMAC object and compute the digest
    h = hmac.new(secret, content, getattr(hashlib, algo_name))
    return h.digest()