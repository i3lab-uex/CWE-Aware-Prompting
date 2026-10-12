import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature of the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    content : bytes
        The data to be signed.
    secret_key : bytes
        Secret key used for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalize algorithm name (hashlib accepts both lower‑case and upper‑case)
    algo_name = algorithm.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Use the hmac module which internally selects a secure HMAC implementation
    return hmac.new(secret_key, content, digestmod=algo_name).digest()