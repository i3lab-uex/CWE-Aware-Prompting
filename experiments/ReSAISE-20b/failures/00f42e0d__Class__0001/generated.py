import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The message to be signed.
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
    # Verify that the hash algorithm is available
    try:
        # Attempt to create a new hash object; this will raise ValueError if unsupported
        hashlib.new(hash_name)
    except (ValueError, TypeError):
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Use HMAC for signing; hmac.new accepts the hash name directly
    mac = hmac.new(key, message, digestmod=hash_name)
    return mac.digest()