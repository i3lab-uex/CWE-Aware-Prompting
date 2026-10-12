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
        The message to be signed.
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
    # Validate that the requested hash function exists in hashlib
    if hash_function_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create the HMAC object and compute the digest
    hmac_obj = hmac.new(sec_key, msg, digestmod=hash_function_name)
    return hmac_obj.digest()