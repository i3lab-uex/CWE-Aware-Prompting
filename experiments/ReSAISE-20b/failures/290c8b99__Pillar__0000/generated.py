import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
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
    # Ensure the requested algorithm exists in hashlib
    if algorithm_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Compute the HMAC signature
    return hmac.new(secret, content, digestmod=algorithm_name).digest()