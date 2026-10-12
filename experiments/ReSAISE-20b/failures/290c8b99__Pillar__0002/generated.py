import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use (e.g. 'sha256', 'md5').
    content : bytes
        The message to be signed.
    secret : bytes
        Secret key used for the HMAC computation.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or unavailable.
    """
    if not isinstance(algorithm_name, str):
        raise TypeError("algorithm_name must be a string")
    if not isinstance(content, bytes):
        raise TypeError("content must be bytes")
    if not isinstance(secret, bytes):
        raise TypeError("secret must be bytes")

    # Normalise algorithm name to lowercase
    algo = algorithm_name.lower()

    # Check that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Create the HMAC object and compute digest
    h = hmac.new(secret, content, digestmod=algo)
    return h.digest()