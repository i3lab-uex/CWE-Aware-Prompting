import hashlib
import hmac

# Secret key used for HMAC signing (must be kept secret and of sufficient length)
secret_key: bytes = b"super_secret_key_which_is_long_and_random"

# Set of hash algorithms considered secure for HMAC
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

def generate_token(hash_algorithm_name: str, payload: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name (hashlib is case‑insensitive but accepts only lower case)
    algo = hash_algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm_name}")

    # Create the HMAC object using the chosen digest
    h = hmac.new(secret_key, msg=payload, digestmod=getattr(hashlib, algo))
    return h.digest()