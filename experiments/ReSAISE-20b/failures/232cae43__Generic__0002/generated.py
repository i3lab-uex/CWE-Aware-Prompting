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
        Data to be signed.
    secret : bytes
        Secret key for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature as raw bytes.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is case‑insensitive and stripped of whitespace
    algo_name = hash_algorithm.strip().lower()

    # Validate that the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")

    # Create the HMAC object using the chosen hash constructor
    hmac_obj = hmac.new(secret, payload, digestmod=hashlib.new(algo_name))
    return hmac_obj.digest()