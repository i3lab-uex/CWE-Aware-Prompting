import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        The name of the hash function to use (e.g., 'sha256', 'md5', etc.).
    content : bytes
        The data to be signed.
    secret_key : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise algorithm name to lower case
    algo = algorithm.lower()

    # Verify that the requested algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm!r}")

    # Create and return the HMAC digest
    hmac_obj = hmac.new(secret_key, content, algo)
    return hmac_obj.digest()