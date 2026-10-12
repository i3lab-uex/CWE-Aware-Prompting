import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (must be supported by hashlib).
    message : bytes
        The data to sign.
    key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available in hashlib.
    """
    # Ensure the algorithm exists
    try:
        hash_func = hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available") from exc

    # Create HMAC object using the same hash function
    hmac_obj = hmac.new(key, msg=message, digestmod=hash_func)
    return hmac_obj.digest()