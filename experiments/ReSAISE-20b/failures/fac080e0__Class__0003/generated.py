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
        The computed HMAC digest of the message.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported.
    """
    # Ensure algorithm is available in this environment
    if algo.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    # Compute HMAC using the standard library's hmac module
    mac = hmac.new(secret_key, msg, digestmod=algo.lower())
    return mac.digest()