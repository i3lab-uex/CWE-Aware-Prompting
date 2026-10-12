import hashlib
import hmac

# List of algorithms that are considered secure for HMAC usage.
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",
    "sha3_224",
    "shake_128",
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

# Optional: map algorithm names to the corresponding hashlib constructor
_HASHLIB_MAP = {name: getattr(hashlib, name) for name in SECURE_ALGORITHMS}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the given content using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a secure hash algorithm supported by hashlib.
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        HMAC signature of the content.

    Raises
    ------
    ValueError
        If the hash algorithm is not supported or considered insecure.
    """
    # Normalize name (hashlib expects lower case names)
    alg_name = hash_algorithm.lower()

    if alg_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # The secret key must be defined securely; for this example we use a static key.
    # In real-world usage, obtain the key from a secure source (e.g., environment variable,
    # HSM, or secrets manager).
    secret_key = b"super-secret-key"

    # Create an HMAC object using the selected hash algorithm
    hmac_obj = hmac.new(secret_key, content, _HASHLIB_MAP[alg_name])
    return hmac_obj.digest()