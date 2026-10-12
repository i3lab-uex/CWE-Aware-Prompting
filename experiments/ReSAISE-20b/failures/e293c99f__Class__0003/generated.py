import hashlib
import hmac

# A secret key used for generating the signature.
# In a real application this should be kept confidential and
# managed securely (e.g., using environment variables or a secrets manager).
secret_key: bytes = b"super_secret_key"

# List of cryptographically secure hash algorithms supported by hashlib.
_SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for `raw_data` using the specified
    hashing algorithm.

    Parameters:
        algo_name (str): Name of the hash function to use.
        raw_data (bytes): Data that will be signed.

    Returns:
        bytes: The HMAC signature.

    Raises:
        ValueError: If the algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name to lower case
    algo_name = algo_name.lower()

    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algo_name}")

    # Retrieve the hashlib constructor for the chosen algorithm
    try:
        hash_func = getattr(hashlib, algo_name)
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm {algo_name} is not available.") from exc

    # Create an HMAC object using the secret key and chosen hash function
    hmac_obj = hmac.new(secret_key, raw_data, digestmod=hash_func)

    # Return the binary digest
    return hmac_obj.digest()