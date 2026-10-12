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
        The key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Normalise algorithm name (hashlib is case‑sensitive)
    algo = hash_algorithm.lower()
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Compute the HMAC using Python's standard library
    return hmac.new(secret, payload, digestmod=algo).digest()