import hashlib
import hmac

def authenticate_message(algorithm: str, content: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC value for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    content : bytes
        The message to be authenticated.
    secret : bytes
        The secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the system.
    """
    # Ensure the algorithm name is valid and available
    if algorithm.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the HMAC object using the selected digest method
    h = hmac.new(secret, content, hashlib.get_digest_by_name(algorithm))
    return h.digest()