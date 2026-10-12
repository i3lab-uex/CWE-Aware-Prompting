import hashlib
import hmac

# Secret key used for signing – in a real application this should be kept secret
# and stored securely (e.g., environment variable, key management service).
secret_key: bytes = b"your-very-secret-key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'sha512').
    data : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the data.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported by hashlib.
    """
    # Verify that the requested hash algorithm is available
    try:
        # Attempt to create a new hash object to confirm availability
        hashlib.new(hash_name)
    except ValueError as exc:
        raise ValueError(f"Unsupported hash algorithm: {hash_name}") from exc

    # Create the HMAC object using the secret key and chosen hash algorithm
    hmac_obj = hmac.new(secret_key, msg=data, digestmod=hash_name)

    # Return the binary signature
    return hmac_obj.digest()