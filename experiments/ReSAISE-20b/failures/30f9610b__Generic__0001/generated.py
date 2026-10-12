import hashlib
import hmac

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Sign the provided message using HMAC with the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hashing function to use (e.g., 'sha256', 'md5').
    data : bytes
        The message to be signed.
    secret_key : bytes
        The secret key used in the HMAC process.

    Returns
    -------
    bytes
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Verify that the requested hashing method exists in hashlib
    try:
        # This will raise a ValueError if the algorithm is not available
        hashlib.new(method_name)
    except (ValueError, TypeError):
        raise ValueError(f"Unsupported or unavailable hash algorithm: {method_name}")

    # Create the HMAC object using the secret key, data, and chosen hash function
    hmac_obj = hmac.new(secret_key, data, digestmod=method_name)

    # Return the raw bytes of the HMAC signature
    return hmac_obj.digest()