import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'md5').
    content : bytes
        The message to be signed.
    secret : bytes
        Secret key used in the HMAC process.

    Returns
    -------
    bytes
        The computed HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or unavailable.
    """
    # Ensure the algorithm name is valid and available
    try:
        # hashlib.new will raise a ValueError if the algorithm is not supported
        hash_func = hashlib.new(algorithm_name)
    except ValueError as exc:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}") from exc

    # Compute HMAC using the provided secret and content
    hmac_obj = hmac.new(secret, msg=content, digestmod=hash_func)
    return hmac_obj.digest()