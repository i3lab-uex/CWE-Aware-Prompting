import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of the given content using the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2s').
    content : bytes
        The message to be authenticated.
    secret : bytes
        The key used for the HMAC computation.

    Returns
    -------
    bytes
        The binary HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python
        installation.
    """
    # Ensure the requested algorithm is available
    if algorithm.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the HMAC object using the chosen hash constructor
    h = hmac.new(secret, msg=content, digestmod=hashlib.new(algorithm.lower()))
    return h.digest()