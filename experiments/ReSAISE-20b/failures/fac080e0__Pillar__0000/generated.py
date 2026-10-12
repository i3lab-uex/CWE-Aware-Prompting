import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2s').
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        Secret key used for HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported by the current Python installation.
    """
    # Validate that the algorithm exists in the available hash functions
    if algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo!r}")

    # Compute HMAC using the chosen algorithm
    mac = hmac.new(secret_key, msg, digestmod=algo.lower())
    return mac.digest()