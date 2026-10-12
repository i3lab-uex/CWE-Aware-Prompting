import hashlib
import hmac

# A globally defined secret key (bytes) used for signing.
# In a real application this should be securely stored and rotated.
secret_key = b"your-very-secure-secret-key"

# A set of cryptographic hash algorithms considered secure.
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
    "sm3",  # SM3 is considered secure in its domain
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate a cryptographic signature for `raw_data` using the specified
    hash algorithm and a global secret key.

    Parameters:
        algo_name (str): Name of the hashing algorithm to use.
        raw_data (bytes): The data to be signed.

    Returns:
        bytes: The HMAC signature of the input data.

    Raises:
        ValueError: If `algo_name` is not in the set of secure algorithms.
    """
    algo = algo_name.lower()
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algo_name}")

    # Create an HMAC object with the chosen hash function.
    h = hmac.new(secret_key, raw_data, digestmod=hashlib.new(algo))
    return h.digest()