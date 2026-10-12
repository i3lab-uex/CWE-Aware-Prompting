import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    content : bytes
        Data to be signed.
    secret_key : bytes
        Secret key used for signing.

    Returns
    -------
    bytes
        The HMAC digest as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is case‑insensitive and valid
    algo_name = algorithm.lower()
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the HMAC object
    hmac_obj = hmac.new(secret_key, content, digestmod=algo_name)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()