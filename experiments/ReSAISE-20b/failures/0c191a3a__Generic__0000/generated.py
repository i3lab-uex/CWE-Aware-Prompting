import hashlib
import hmac

# Secret key used for signing. In a real system this should be stored securely.
secret_key = b'super-secret-key'

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Args:
        hash_name: Name of the hash algorithm (e.g., 'sha256', 'sha512').
        data: Data to be signed.

    Returns:
        bytes: The HMAC signature of the data.

    Raises:
        ValueError: If the specified hash algorithm is not available.
    """
    # Verify that the requested hash algorithm exists in hashlib
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Retrieve the hash constructor
    try:
        hash_constructor = getattr(hashlib, hash_name)
    except AttributeError:
        # This should not happen if algorithms_available contains the name,
        # but we guard against it just in case.
        raise ValueError(f"Hash algorithm '{hash_name}' is not supported by hashlib.")

    # Create the HMAC object and compute the signature
    hmac_obj = hmac.new(secret_key, data, hash_constructor)
    return hmac_obj.digest()