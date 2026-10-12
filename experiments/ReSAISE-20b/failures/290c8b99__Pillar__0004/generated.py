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
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalise algorithm name to lower case
    algo = algorithm_name.lower()

    # Check if the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Obtain the constructor for the chosen hash function
    try:
        digestmod = getattr(hashlib, algo)
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not implemented.") from exc

    # Create the HMAC object and compute the digest
    h = hmac.new(secret, content, digestmod=digestmod)
    return h.digest()