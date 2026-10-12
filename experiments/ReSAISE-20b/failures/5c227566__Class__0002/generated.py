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
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Ensure the requested algorithm exists in hashlib
    available_algorithms = {alg.lower() for alg in hashlib.algorithms_available}
    if hash_function_name.lower() not in available_algorithms:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {hash_function_name}")

    # Create the HMAC object with the chosen hash function
    try:
        hmac_obj = hmac.new(sec_key, msg, digestmod=hash_function_name.lower())
    except (TypeError, ValueError) as exc:
        # This catches cases where the algorithm name is not recognized by hmac
        raise ValueError(f"Failed to create HMAC with algorithm '{hash_function_name}': {exc}") from exc

    return hmac_obj.digest()