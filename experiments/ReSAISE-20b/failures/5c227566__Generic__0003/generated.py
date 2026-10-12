import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Generate an HMAC signature for a message using the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hashing function to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to be signed.
    sec_key : bytes
        Secret key used in the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Ensure the requested hash function exists in hashlib
    if hash_function_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create and compute the HMAC signature
    hmac_obj = hmac.new(sec_key, msg, digestmod=hash_function_name)
    return hmac_obj.digest()