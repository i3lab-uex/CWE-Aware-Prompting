import hashlib
import hmac

# Secret key used for signing (must be kept confidential)
secret_key: bytes = b"your-very-secure-secret-key"

def generate_signature(hash_name: str, data: bytes) -> bytes:
    """
    Generate a digital signature for the given data using HMAC with the specified hash algorithm.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g., 'sha256', 'blake2b', etc.).
    data : bytes
        Data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the data.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported by hashlib.
    """
    # Verify that the requested hash algorithm is available
    try:
        # This will raise a ValueError if the name is unknown
        hashlib.new(hash_name)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Unsupported hash algorithm: {hash_name}") from exc

    # Create an HMAC object using the secret key and chosen hash algorithm
    h = hmac.new(secret_key, msg=data, digestmod=hash_name)
    return h.digest()