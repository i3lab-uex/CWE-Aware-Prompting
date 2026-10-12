import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC of the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        The name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    content : bytes
        The message to be authenticated.
    secret : bytes
        The key used for the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python
        installation or if the key/ message arguments are not bytes.
    """
    # Ensure inputs are of correct type
    if not isinstance(content, (bytes, bytearray)):
        raise TypeError("content must be bytes-like")
    if not isinstance(secret, (bytes, bytearray)):
        raise TypeError("secret must be bytes-like")

    # Normalize algorithm name to lower case for comparison
    algo_name = algorithm.lower()

    # Verify that the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Compute the HMAC
    return hmac.new(secret, content, digestmod=algo_name).digest()