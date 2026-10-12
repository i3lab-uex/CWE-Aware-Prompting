import hashlib
import hmac

# A global secret key used for HMAC signing. In a real application this
# should be securely stored (e.g., environment variable, vault) and never
# hard‑coded.
SECRET_KEY = b"super_secret_key_used_for_hmac_signing"

# Algorithms considered cryptographically secure for this use‑case.
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
    "sm3",   # SM3 is considered secure in many contexts
}

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate a cryptographic HMAC signature for the given payload using
    the specified hash algorithm.

    Parameters:
        hash_algorithm_name (str): Name of the hash algorithm to use.
        payload (bytes): Data to be signed.

    Returns:
        bytes: HMAC digest of the payload.

    Raises:
        ValueError: If the algorithm is unsupported or insecure.
        RuntimeError: If a secret key has not been provided.
    """
    if SECRET_KEY is None:
        raise RuntimeError("Secret key for HMAC signing is not set.")

    # Validate that the algorithm exists and is considered secure.
    if hash_algorithm_name.lower() not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm_name}")

    # Retrieve the constructor for the hash function from hashlib.
    try:
        hash_func = getattr(hashlib, hash_algorithm_name.lower())
    except AttributeError as exc:
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is not available.") from exc

    # Create the HMAC object and compute the digest.
    hmac_obj = hmac.new(SECRET_KEY, payload, hash_func)
    return hmac_obj.digest()