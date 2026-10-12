import hashlib
import hmac

def compute_hmac(hash_algorithm: str, payload: bytes, secret: bytes) -> bytes:
    """
    Compute an HMAC signature for the given payload using the specified hash algorithm.

    Args:
        hash_algorithm (str): Name of the hash function to use.
        payload (bytes): Data to be signed.
        secret (bytes): Secret key for HMAC.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the specified hash algorithm is not supported by hashlib.
    """
    # Verify that the requested hash function exists in hashlib
    try:
        # Attempt to create a new hash object; this will raise a ValueError if unsupported
        hashlib.new(hash_algorithm)
    except (ValueError, TypeError):
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}") from None

    # Compute the HMAC using the provided secret and hash algorithm
    hmac_obj = hmac.new(secret, payload, digestmod=hash_algorithm)
    return hmac_obj.digest()