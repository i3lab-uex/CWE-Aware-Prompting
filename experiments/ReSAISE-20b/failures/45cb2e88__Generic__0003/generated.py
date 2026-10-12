import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature of the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to sign.
    secret_key : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The computed HMAC signature as raw bytes.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is valid and available in hashlib
    if algorithm.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    # Create a new HMAC object with the specified key and hash function
    hmac_obj = hmac.new(secret_key, content, digestmod=algorithm.lower())

    # Return the raw bytes of the HMAC signature
    return hmac_obj.digest()