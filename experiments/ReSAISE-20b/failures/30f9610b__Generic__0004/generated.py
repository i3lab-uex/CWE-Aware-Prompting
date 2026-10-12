import hmac
import hashlib

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hashing function to use (e.g. 'sha256', 'md5').
    data : bytes
        The message to be signed.
    secret_key : bytes
        The secret key used for HMAC.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalize method name and validate availability
    algo = method_name.lower()
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported or unavailable hash algorithm: {method_name}")

    # Create a new HMAC object using the chosen digest constructor
    try:
        digest = hashlib.new(algo)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Could not initialize hash algorithm '{method_name}': {exc}") from exc

    hmac_obj = hmac.new(secret_key, data, digest)
    return hmac_obj.digest()