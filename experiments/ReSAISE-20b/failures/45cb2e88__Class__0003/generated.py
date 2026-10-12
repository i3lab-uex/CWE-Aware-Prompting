import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2b', etc.).
    content : bytes
        The data to be signed.
    secret_key : bytes
        The key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature (raw digest bytes).

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Ensure the algorithm name is case‑insensitive and normalised
    algo_name = algorithm.lower()

    # Validate that the algorithm is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create a new HMAC object with the chosen algorithm
    hmac_obj = hmac.new(secret_key, content, getattr(hashlib, algo_name))

    # Return the raw digest bytes
    return hmac_obj.digest()