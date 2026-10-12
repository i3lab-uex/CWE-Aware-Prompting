import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm and secret key.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'md5').
    content : bytes
        The message to be signed.
    secret : bytes
        Secret key used for the HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or unavailable.
    """
    # Normalize the algorithm name to lowercase and strip whitespace
    algo = algorithm_name.strip().lower()

    # Verify that the requested algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Use the hmac module to compute the signature securely
    mac = hmac.new(secret, content, digestmod=algo)
    return mac.digest()