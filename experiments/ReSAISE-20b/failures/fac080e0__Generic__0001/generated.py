import hashlib
import hmac

def verify_signature(algo: str, msg: bytes, secret_key: bytes) -> bytes:
    """
    Compute the HMAC of a message using the specified hash algorithm and secret key.

    Parameters
    ----------
    algo : str
        Name of the hash algorithm to use (e.g. 'sha256', 'md5', etc.).
    msg : bytes
        The message to authenticate.
    secret_key : bytes
        Secret key used for the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib on this system.
    """
    try:
        # Verify that the algorithm exists and is supported
        hash_func = hashlib.new(algo)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm: {algo}") from exc

    # Use the hash function as the digestmod argument for hmac
    return hmac.new(secret_key, msg, digestmod=hash_func).digest()