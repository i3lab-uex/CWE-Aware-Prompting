import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Create an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        The name of the hash function to use (e.g., 'sha256', 'blake2s').
    content : bytes
        The data to be signed.
    secret_key : bytes
        The secret key used for signing.

    Returns
    -------
    bytes
        The computed HMAC signature as raw bytes.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise algorithm name (hashlib expects the canonical form)
    algo = algorithm.lower()

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the HMAC object using the requested hash function
    hmac_obj = hmac.new(secret_key, content, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()