import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of `content` using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    content : bytes
        The message to authenticate.
    secret : bytes
        Secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available on this system.
    """
    # Ensure the algorithm name is case‑insensitive and supported
    alg = algorithm.lower()
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Use the standard library hmac module which is secure against timing attacks
    return hmac.new(secret, content, digestmod=alg).digest()