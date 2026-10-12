import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash function to use (case‑insensitive).
    content : bytes
        The message to be signed.
    secret : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If the specified algorithm is not available in hashlib.
    """
    # Normalise algorithm name to lowercase
    algo = algorithm_name.lower()

    # Verify that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm_name}")

    # Create the HMAC object
    h = hmac.new(secret, content, digestmod=algo)

    # Return the raw bytes of the HMAC
    return h.digest()