import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hashing function to use (e.g. 'sha256', 'md5', etc.).
    data : bytes
        The message to be signed.
    secret_key : bytes
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The resulting HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or available.
    """
    # Normalise name to lowercase for comparison
    algo = method_name.lower()

    # Verify that the algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {method_name}")

    # Create a new HMAC object using the chosen digest
    h = hmac.new(secret_key, data, digestmod=hashlib.new(algo))
    return h.digest()