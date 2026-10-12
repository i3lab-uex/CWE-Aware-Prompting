import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hash function to use (e.g. 'sha256', 'md5').
    msg : bytes
        The message to be signed.
    sec_key : bytes
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The resulting HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or unavailable.
    """
    # Normalise the algorithm name
    algo = hash_function_name.lower()

    # Verify that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create the HMAC object
    hmac_obj = hmac.new(sec_key, msg, digestmod=algo)

    # Return the raw bytes of the HMAC signature
    return hmac_obj.digest()