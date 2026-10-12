import hmac
import hashlib

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC of ``msg`` using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    msg : bytes
        The message to be authenticated.
    secret_key : bytes
        The secret key used for the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported on this system.
    """
    # Ensure the algorithm name is valid and available
    if algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(secret_key, msg, hashlib.new(algo.lower()))
    return hmac_obj.digest()