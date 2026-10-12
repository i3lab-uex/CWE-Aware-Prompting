import hashlib
import hmac

def sign_message(hash_name: str, message: bytes, key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    message : bytes
        The data to be signed.
    key : bytes
        Secret key used for HMAC signing.

    Returns
    -------
    bytes
        The HMAC digest of the message.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Verify that the hash algorithm exists in hashlib
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Create a new HMAC object using the specified hash algorithm
    try:
        hmac_obj = hmac.new(key, msg=message, digestmod=hash_name)
    except TypeError as exc:
        # This can happen if the hash name is not a valid digestmod
        raise ValueError(f"Invalid hash algorithm '{hash_name}'.") from exc

    # Return the digest as bytes
    return hmac_obj.digest()