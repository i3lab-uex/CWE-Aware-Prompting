import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use.
    message : bytes
        The message to sign.
    key : bytes
        Secret key used for signing.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported.
    """
    # Verify that the requested hash algorithm exists
    try:
        hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm: {hash_name}") from exc

    # Compute the HMAC digest
    hmac_obj = hmac.new(key, msg=message, digestmod=hash_name)
    return hmac_obj.digest()