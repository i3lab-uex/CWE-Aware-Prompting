import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s').
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
        If the requested hash algorithm is not available in hashlib.
    """
    # Normalize the algorithm name (hashlib uses lowercase names)
    algo_name = hash_algorithm.lower()

    # Verify that the algorithm is supported
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(secret, payload, hashlib.new(algo_name))
    return hmac_obj.digest()