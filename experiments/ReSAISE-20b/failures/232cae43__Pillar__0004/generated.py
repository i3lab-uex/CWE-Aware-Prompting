import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b', ...).
    payload : bytes
        The data to be signed.
    secret : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the hash algorithm is available in the current Python environment
    if hash_algorithm.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create a new HMAC object using the specified digest function
    hmac_obj = hmac.new(secret, payload, digestmod=hash_algorithm.lower())

    # Return the computed HMAC signature as bytes
    return hmac_obj.digest()