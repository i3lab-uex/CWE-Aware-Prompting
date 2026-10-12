import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hashing function to use (e.g., 'sha256', 'md5').
    msg : bytes
        The message to sign.
    sec_key : bytes
        Secret key for the HMAC.

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
    if not hasattr(hashlib, hash_function_name):
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create a new HMAC object with the chosen digest mode
    try:
        hmac_obj = hmac.new(sec_key, msg, getattr(hashlib, hash_function_name))
    except TypeError as exc:
        # This catches cases where the algorithm is not a valid digest constructor
        raise ValueError(f"Hash function '{hash_function_name}' cannot be used: {exc}") from exc

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()