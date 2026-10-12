import hashlib
import hmac

# A secret key used for signing. In a real application this must be kept
# confidential and managed securely (e.g., via environment variables or a secrets manager).
secret_key = b"super_secret_key_that_should_be_at_least_32_bytes_long"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Args:
        hash_name: Name of a hashlib-supported hash function.
        data: The binary data to sign.

    Returns:
        A byte string containing the HMAC signature.

    Raises:
        ValueError: If the requested hash algorithm is not available.
    """
    # Verify that the hash algorithm exists
    try:
        hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Hash algorithm '{hash_name}' is not available.") from exc

    # Compute the HMAC signature
    hmac_obj = hmac.new(secret_key, data, digestmod=hash_name)
    return hmac_obj.digest()