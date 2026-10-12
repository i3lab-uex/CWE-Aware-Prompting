import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        The name of the hash algorithm to use (e.g. 'sha256', 'md5').
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        The secret key used for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported on this system.
    """
    # Ensure the algorithm is available in the current Python environment
    if algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo!r}")

    # Create a new HMAC object with the given key and hash algorithm
    h = hmac.new(secret_key, msg, digestmod=algo.lower())
    return h.digest()