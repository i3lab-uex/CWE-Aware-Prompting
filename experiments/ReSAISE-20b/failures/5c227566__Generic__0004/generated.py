import hashlib
import hmac

def create_signature(hash_function_name: str, msg: bytes, sec_key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm and secret key.

    Parameters
    ----------
    hash_function_name : str
        Name of the hashing algorithm to use (e.g. 'sha256', 'md5', etc.).
    msg : bytes
        The message to be signed.
    sec_key : bytes
        Secret key used in the HMAC process.

    Returns
    -------
    bytes
        The computed HMAC signature as raw bytes.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalise name to lower-case (hashlib uses lower-case names)
    algo_name = hash_function_name.lower()

    # Verify that the algorithm is available
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create a new HMAC object using the chosen hash function
    try:
        hmac_obj = hmac.new(sec_key, msg, digestmod=algo_name)
    except Exception as exc:
        # hmac.new may raise a TypeError if the digestmod is not callable or invalid
        raise ValueError(f"Failed to create HMAC with algorithm {hash_function_name}: {exc}") from exc

    # Return the raw digest bytes
    return hmac_obj.digest()