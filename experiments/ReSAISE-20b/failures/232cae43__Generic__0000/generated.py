import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The name of the hash function to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        The data to be signed.
    secret : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is supported
    if hash_algorithm.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Use the hmac module for a constant‑time implementation
    return hmac.new(secret, payload, digestmod=hash_algorithm).digest()