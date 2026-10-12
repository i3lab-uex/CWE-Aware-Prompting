import hmac
import hashlib

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    content : bytes
        The message to be authenticated.
    secret : bytes
        Secret key used for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC value.

    Raises
    ------
    ValueError
        If the requested algorithm is not available on this system.
    """
    # Normalise algorithm name to lower case
    algo_name = algorithm.lower()

    # Verify that the algorithm is supported by hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create a new hash object using the specified algorithm
    hash_obj = hashlib.new(algo_name)

    # Compute HMAC with the provided secret and content
    hmac_obj = hmac.new(secret, content, hash_obj)
    return hmac_obj.digest()