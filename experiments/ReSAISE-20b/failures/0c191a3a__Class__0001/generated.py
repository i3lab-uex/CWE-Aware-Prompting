import hashlib
import hmac

# Secret key used for signing (should be kept secret and random)
secret_key: bytes = b'super_secret_key_please_change'

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Args:
        hash_name: The name of the hash algorithm (e.g., 'sha256', 'sha512').
        data: The data to be signed.

    Returns:
        bytes: The HMAC signature of the data.

    Raises:
        ValueError: If the requested hash algorithm is not available.
    """
    # Normalize algorithm name (hashlib uses lower case)
    hash_name = hash_name.lower()

    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available on this system.")

    # Create HMAC object with the chosen hash function
    hmac_obj = hmac.new(secret_key, data, digestmod=hash_name)

    # Return the raw bytes of the signature
    return hmac_obj.digest()