import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'sha512').
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
        If the requested hash algorithm is not supported by hashlib.
    """
    # Validate that the chosen hash algorithm exists in hashlib
    if hash_algorithm.lower() not in {alg.lower() for alg in hashlib.algorithms_available}:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create and compute the HMAC using the chosen digest method
    h = hmac.new(secret, payload, digestmod=hash_algorithm)
    return h.digest()