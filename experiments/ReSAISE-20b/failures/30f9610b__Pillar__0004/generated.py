import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    data : bytes
        The message to sign.
    secret_key : bytes
        Secret key for the HMAC operation.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or unavailable.
    """
    # Normalise method name to lowercase for consistency
    algo = method_name.lower()

    # Check if the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {method_name}")

    # Create the HMAC object and compute the digest
    h = hmac.new(secret_key, data, algo)
    return h.digest()