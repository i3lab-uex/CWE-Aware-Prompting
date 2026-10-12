import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to be signed.
    sec_key : bytes
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The generated HMAC signature (raw digest).

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Ensure the requested hash algorithm is available
    if hash_function_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create the HMAC object with the specified hash function
    hmac_obj = hmac.new(sec_key, msg, getattr(hashlib, hash_function_name.lower()))
    return hmac_obj.digest()