import hashlib
import hmac

def create_hmac_signature(algorithm: str, content: bytes, secret_key: bytes) -> bytes:
    """
    Compute an HMAC signature of the given content using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    content : bytes
        The data to be signed.
    secret_key : bytes
        The secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature as raw bytes.

    Raises
    ------
    ValueError
        If the specified algorithm is not supported by hashlib.
    """
    # Normalize the algorithm name to lowercase
    algo_name = algorithm.lower()

    # Ensure the requested hash function is available in hashlib
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    # Create the HMAC object using the chosen digest function
    hmac_obj = hmac.new(secret_key, content, digestmod=algo_name)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()