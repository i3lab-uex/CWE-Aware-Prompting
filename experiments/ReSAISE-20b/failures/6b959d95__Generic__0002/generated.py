import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of the given content using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s', etc.).
    content : bytes
        The message to be authenticated.
    secret : bytes
        Secret key used for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value (raw digest).

    Raises
    ------
    ValueError
        If the specified algorithm is not supported on this system.
    """
    # Normalise algorithm name to lowercase for consistency
    algo = algorithm.lower()

    # Ensure the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create HMAC object with the chosen digestmod
    h = hmac.new(secret, msg=content, digestmod=algo)

    # Return raw bytes of the HMAC
    return h.digest()