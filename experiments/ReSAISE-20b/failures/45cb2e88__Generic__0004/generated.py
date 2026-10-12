import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'blake2s').
    content : bytes
        The message to be signed.
    secret_key : bytes
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
    # Ensure the algorithm name is case‑insensitive and stripped
    alg = algorithm.strip().lower()

    # Verify that the requested hash function is available in hashlib
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    # Compute HMAC using the chosen digest method
    return hmac.new(secret_key, content, digestmod=alg).digest()