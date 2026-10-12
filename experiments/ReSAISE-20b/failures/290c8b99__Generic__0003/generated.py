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
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The generated HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported or unavailable.
    """
    # Ensure algorithm name is case‑insensitive and stripped
    algo = algorithm_name.strip().lower()

    # Validate that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{algorithm_name}'")

    # Create a new HMAC object with the chosen digest constructor
    try:
        hmac_obj = hmac.new(secret, msg=content, digestmod=getattr(hashlib, algo))
    except AttributeError:
        # Fallback for algorithms that are not exposed as attributes
        hmac_obj = hmac.new(secret, msg=content, digestmod=hashlib.new(algo))

    # Return the raw bytes of the digest
    return hmac_obj.digest()