import hashlib
import hmac

# Secret key used for HMAC. In a real application this should be stored securely.
SECRET_KEY: bytes = b"super_secret_key_which_must_be_kept_safe"

# Set of hash algorithms considered secure for HMAC
SECURE_ALGORITHMS = {
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
    Generate a cryptographic HMAC signature for the provided data using
    the specified hash algorithm.

    Parameters:
        algo_name (str): Name of the hashing algorithm to use.
        raw_data (bytes): Data that needs to be signed.

    Returns:
        bytes: The generated HMAC signature.

    Raises:
        ValueError: If an unsupported or insecure algorithm is specified.
    """
    algo_name = algo_name.lower()
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algo_name}. "
            f"Supported algorithms are: {', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create HMAC using the chosen hash algorithm
    hmac_obj = hmac.new(SECRET_KEY, raw_data, getattr(hashlib, algo_name))
    return hmac_obj.digest()