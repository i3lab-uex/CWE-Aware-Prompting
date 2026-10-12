import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing function to use (e.g., 'sha256', 'md5').
    content : bytes
        The message to be signed.
    secret : bytes
        Secret key used in the HMAC process.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or available.
    """
    # Normalise algorithm name (case-insensitive)
    algo = algorithm_name.lower()

    # Check if the algorithm is available in this Python build
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not supported or available.")

    # Create a new HMAC object with the chosen hash constructor
    h = hmac.new(secret, msg=content, digestmod=getattr(hashlib, algo))
    return h.digest()