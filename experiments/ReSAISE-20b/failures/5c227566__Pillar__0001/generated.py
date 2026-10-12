import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Create an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to sign.
    sec_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or unavailable.
    """
    # Validate that the hash function exists in hashlib
    try:
        _ = hashlib.new(hash_function_name)
    except (AttributeError, ValueError):
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create the HMAC object using the specified hash function
    hmac_obj = hmac.new(sec_key, msg, digestmod=hash_function_name)
    return hmac_obj.digest()