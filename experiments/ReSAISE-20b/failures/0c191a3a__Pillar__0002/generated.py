import hashlib
import hmac

# A secret key used for signing. In a real application this must be kept
# secure and not hard‑coded.
secret_key: bytes = b"your-very-secure-secret-key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC and the
    specified hash algorithm.

    Args:
        hash_name (str): The name of the hash algorithm to use.
        data (bytes): The data to be signed.

    Returns:
        bytes: The HMAC signature of the data.

    Raises:
        ValueError: If the requested hash algorithm is not available.
    """
    # Ensure the hash algorithm exists in the current Python environment
    if hash_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.")

    # Compute the HMAC using the secret key and chosen hash algorithm
    return hmac.new(secret_key, data, digestmod=hash_name).digest()