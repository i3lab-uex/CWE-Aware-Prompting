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
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalize algorithm name to lowercase
    alg = algorithm_name.lower()

    # Check if the algorithm is available in hashlib
    try:
        hash_func = getattr(hashlib, alg)
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not supported.") from exc

    # Verify that the function can be called without arguments
    try:
        hash_func()
    except TypeError as exc:
        raise ValueError(f"Hash algorithm '{algorithm_name}' cannot be instantiated.") from exc

    # Create and return the HMAC signature
    h = hmac.new(secret, content, digestmod=hash_func)
    return h.digest()