import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Generate an HMAC signature for a given message using the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hashing function to use (e.g., 'sha256', 'md5', etc.).
    msg : bytes
        The message to be signed.
    sec_key : bytes
        Secret key used in the HMAC process.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    TypeError
        If `msg` or `sec_key` are not bytes objects.
    """
    # Validate input types
    if not isinstance(msg, (bytes, bytearray)):
        raise TypeError("msg must be a bytes-like object")
    if not isinstance(sec_key, (bytes, bytearray)):
        raise TypeError("sec_key must be a bytes-like object")

    # Ensure the hash function is available in hashlib
    try:
        # hashlib.new will raise a ValueError if the algorithm is not supported
        hashlib.new(hash_function_name)
    except (ValueError, TypeError):
        raise ValueError(f"Hash algorithm '{hash_function_name}' is not supported")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(sec_key, msg, digestmod=hash_function_name)
    return hmac_obj.digest()