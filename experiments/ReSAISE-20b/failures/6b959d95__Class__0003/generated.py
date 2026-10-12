import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute the HMAC of `content` using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    content : bytes
        The message to be authenticated.
    secret : bytes
        The secret key for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value as a byte string.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on this system.
    """
    # Normalize algorithm name to lower case
    algo = algorithm.lower()

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create a new HMAC object with the chosen digest mode
    hmac_obj = hmac.new(secret, content, hashlib.new(algo))
    return hmac_obj.digest()