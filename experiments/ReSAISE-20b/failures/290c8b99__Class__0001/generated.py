import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'md5', etc.).
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
        If the specified algorithm is not supported or available.
    """
    # Ensure the algorithm name is in a consistent case
    alg = algorithm_name.lower()

    # Validate that the requested algorithm exists in hashlib.algorithms_available
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Create a new HMAC object with the chosen hash function
    try:
        h = hmac.new(secret, content, digestmod=alg)
    except TypeError as exc:
        # This can happen if the algorithm name is accepted but the digestmod
        # cannot be constructed (e.g., due to a broken implementation).
        raise ValueError(f"Failed to initialize HMAC with algorithm {algorithm_name}") from exc

    # Return the raw bytes of the digest
    return h.digest()