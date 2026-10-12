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
        Secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC value as a byte string.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib on this system.
    """
    # Normalize algorithm name to lower case for comparison
    alg_name = algorithm.lower()

    # Ensure the requested algorithm is available in hashlib
    if alg_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Retrieve the corresponding constructor from hashlib
    hash_constructor = getattr(hashlib, alg_name)

    # Compute HMAC using the selected hash function
    hmac_obj = hmac.new(secret, content, digestmod=hash_constructor)
    return hmac_obj.digest()