import hashlib
import hmac

# Secret key used for HMAC signing (must be kept confidential)
secret_key: bytes = b"your-very-secret-key"

# Set of cryptographically secure hash algorithms supported by hashlib
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'blake2b').
    raw_data : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the algorithm name is unsupported or considered insecure.
    """
    # Normalise algorithm name (hashlib uses lower case names)
    algo = algo_name.lower()

    # Validate that the algorithm is secure and available
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algo_name}")

    # Retrieve the constructor for the chosen hash function
    try:
        hash_func = getattr(hashlib, algo)
    except AttributeError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm not available in hashlib: {algo_name}") from exc

    # Create an HMAC object using the secret key and chosen hash function
    hmac_obj = hmac.new(secret_key, raw_data, digestmod=hash_func)

    # Return the resulting signature bytes
    return hmac_obj.digest()