import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to be signed.
    secret_key : bytes
        Secret key used for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC signature as raw bytes.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Normalise the algorithm name to match hashlib's naming
    algo_name = algorithm.lower()

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    # Create the HMAC object using the chosen digest function
    hmac_obj = hmac.new(secret_key, content, digestmod=hashlib.new(algo_name))

    return hmac_obj.digest()