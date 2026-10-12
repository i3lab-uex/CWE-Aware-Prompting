import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_function_name : str
        Name of the hash function to use (e.g. 'sha256', 'blake2b').
    msg : bytes
        The message to sign.
    sec_key : bytes
        Secret key for the HMAC operation.

    Returns
    -------
    bytes
        The resulting HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalise name to lowercase for comparison
    alg_name = hash_function_name.lower()

    # Verify algorithm is available in the current hashlib implementation
    if alg_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_function_name}")

    # Create the HMAC object
    hmac_obj = hmac.new(sec_key, msg, digestmod=alg_name)

    # Return the raw bytes of the signature
    return hmac_obj.digest()