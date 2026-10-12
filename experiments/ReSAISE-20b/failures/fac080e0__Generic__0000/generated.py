import hmac
import hashlib

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        The name of the hash algorithm to use (e.g., 'sha256', 'md5', etc.).
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        The secret key used for HMAC generation.

    Returns
    -------
    bytes
        The computed HMAC value as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by the current system.
    """
    # Normalise algorithm name to lowercase for consistency
    algo_lower = algo.lower()

    # Verify that the algorithm is available in hashlib
    if algo_lower not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Create a new HMAC object using the selected algorithm
    h = hmac.new(secret_key, msg, getattr(hashlib, algo_lower))
    
    # Return the digest as bytes
    return h.digest()