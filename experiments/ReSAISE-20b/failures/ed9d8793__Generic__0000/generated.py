import hashlib
import hmac

# A global secret key used for HMAC signing. In a real application this
# should be securely generated and stored (e.g., in an environment variable
# or a secrets manager). For demonstration purposes we use a static key.
secret_key: bytes = b"super_secret_key_used_for_hmac_signing"

# Whitelist of secure hash algorithms suitable for HMAC signing.
SECURE_HASH_ALGORITHMS = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    "sha512_224",
    "sha512_256",
}

def sign_data(hash_algorithm: str, content: bytes) -> bytes:
    """
    Generate an HMAC signature for the provided data using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256').
    content : bytes
        Data that should be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the requested hash algorithm is not supported or considered insecure.
    """
    # Normalise the algorithm name to lower case to avoid case‑sensitivity issues
    algo = hash_algorithm.lower()

    # Validate that the algorithm is available in hashlib and is on our whitelist
    if algo not in SECURE_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{hash_algorithm}'. "
            f"Supported algorithms: {', '.join(sorted(SECURE_HASH_ALGORITHMS))}"
        )

    # Compute the HMAC signature
    hmac_obj = hmac.new(secret_key, content, digestmod=algo)
    return hmac_obj.digest()