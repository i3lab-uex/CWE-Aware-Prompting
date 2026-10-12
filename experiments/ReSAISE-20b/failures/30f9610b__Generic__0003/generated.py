import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Sign a message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hash function to use (e.g., 'sha256', 'md5').
    data : bytes
        The message to sign.
    secret_key : bytes
        The secret key for HMAC.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Validate input types (optional but helpful)
    if not isinstance(data, bytes):
        raise TypeError("data must be of type 'bytes'")
    if not isinstance(secret_key, bytes):
        raise TypeError("secret_key must be of type 'bytes'")

    # Ensure the hash algorithm is available
    try:
        hash_func = hashlib.new(method_name)
    except (ValueError, TypeError):
        raise ValueError(f"Unsupported or unavailable hash algorithm: '{method_name}'")

    # Compute HMAC using the selected hash function
    hmac_obj = hmac.new(secret_key, data, digestmod=hash_func)
    return hmac_obj.digest()