import hashlib
import hmac

# Replace this with your actual secret key (bytes).
# It should be kept confidential and stored securely.
secret_key: bytes = b"your-very-secret-key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b', etc.).
    data : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC digest (digital signature) of the data.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Verify that the requested hash algorithm exists in hashlib
    if hash_name.lower() not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {hash_name}")

    # Create an HMAC object using the secret key and specified hash function
    hmac_obj = hmac.new(secret_key, msg=data, digestmod=hash_name)

    # Return the raw bytes of the HMAC digest
    return hmac_obj.digest()