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
        The data that should be signed.
    key : bytes
        Secret key used for signing.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not available.
    """
    # Ensure the hash algorithm is supported by hashlib
    if hash_name.lower() not in {name.lower() for name in hashlib.algorithms_available}:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Compute the HMAC digest using the requested hash algorithm
    mac = hmac.new(key, message, hash_name)
    return mac.digest()