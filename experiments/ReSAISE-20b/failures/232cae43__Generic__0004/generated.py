import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        The data to be signed.
    secret : bytes
        The secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is valid (case-insensitive)
    alg_name = hash_algorithm.lower()
    if alg_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(secret, payload, digestmod=alg_name)
    return hmac_obj.digest()