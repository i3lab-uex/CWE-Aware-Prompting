import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b', ...).
    message : bytes
        The data to sign.
    key : bytes
        Secret key used for signing.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Normalise the hash name to lower case (hashlib is case‑insensitive but
    # we keep a canonical form for error messages).
    hash_name = hash_name.lower()

    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available")

    # Use the hmac module which implements a constant‑time comparison
    # and follows best practices for HMAC construction.
    h = hmac.new(key, msg=message, digestmod=hash_name)
    return h.digest()