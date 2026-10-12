import hashlib
import hmac

def generate_signature(algorithm_name: str, content: bytes, secret: bytes) -> bytes:
    """
    Sign the provided message using HMAC with the specified hash algorithm.

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
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or available.
    """
    # Normalize algorithm name to lower case for consistency
    alg = algorithm_name.lower()

    # Verify that the algorithm is available in hashlib
    if alg not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {algorithm_name}")

    # Create the HMAC object with the chosen digestmod
    hmac_obj = hmac.new(secret, content, digestmod=alg)

    # Return the raw bytes of the signature
    return hmac_obj.digest()