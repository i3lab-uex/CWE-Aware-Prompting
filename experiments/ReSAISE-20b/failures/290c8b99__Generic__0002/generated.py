import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    content : bytes
        The message to be signed.
    secret : bytes
        The secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Ensure the requested algorithm is available in hashlib
    try:
        # hashlib.new will raise a ValueError if the name is unknown
        _ = hashlib.new(algorithm_name)
    except (ValueError, TypeError):
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name!r}")

    # Compute the HMAC signature
    hmac_obj = hmac.new(secret, content, digestmod=algorithm_name)
    return hmac_obj.digest()