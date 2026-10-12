import hmac
import hashlib

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
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or unavailable.
    """
    # Normalise algorithm name to lower case for consistency
    algo = algorithm_name.lower()

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Create HMAC object with the chosen digest mode
    h = hmac.new(secret, content, digestmod=algo)

    # Return the raw bytes of the HMAC digest
    return h.digest()