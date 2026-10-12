import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'md5', etc.).
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
    # Validate that the hash algorithm exists
    try:
        hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm: {hash_name}") from exc

    # Compute HMAC using the chosen hash function
    return hmac.new(key, message, hash_name).digest()