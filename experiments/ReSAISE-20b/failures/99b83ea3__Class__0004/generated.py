import hashlib
import hmac

# A pre‑shared secret key used for HMAC signing.
# In a real system this should be stored securely (e.g. in a key vault).
SECRET_KEY: bytes = b"super_secret_key_please_change"

# List of cryptographically secure hash algorithms supported by hashlib.
SECURE_ALGORITHMS = {
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

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for *message* using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g. "sha256").
    message : bytes
        The data to sign.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If *algorithm_name* is not supported or considered insecure.
    """
    # Normalise the algorithm name (hashlib accepts lower‑case names).
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}. "
            f"Supported algorithms are: {', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Retrieve the hash constructor from hashlib.
    hash_func = getattr(hashlib, algo)

    # Compute HMAC using the chosen hash algorithm.
    return hmac.new(SECRET_KEY, message, hash_func).digest()