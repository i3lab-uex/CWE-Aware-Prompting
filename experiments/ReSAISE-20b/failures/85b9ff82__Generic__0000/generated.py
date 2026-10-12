import hashlib
import hmac

# --- Configuration ----------------------------------------------------------
# Secret key used for HMAC.  In a real application this would be stored
# securely (e.g., environment variable, key management system).
SECRET_KEY: bytes = b"super_secret_key_please_change"

# Set of hash algorithms that are considered secure for this project.
# We deliberately exclude MD5, SHA‑1, and the variable‑length SHAKE functions
# because they are no longer recommended for cryptographic use.
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

# ---------------------------------------------------------------------------

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Compute an HMAC signature of ``content`` using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of a cryptographic hash algorithm (e.g., "sha256").
    content : bytes
        Raw data to sign.

    Returns
    -------
    bytes
        The HMAC signature.

    Raises
    ------
    ValueError
        If ``hash_algorithm`` is not supported or is disallowed.
    """
    # Normalise algorithm name to lowercase for comparison
    algo = hash_algorithm.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {hash_algorithm!r}"
        )

    # Ensure the chosen algorithm is available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(
            f"Hash algorithm {hash_algorithm!r} is not available on this system."
        )

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, content, digestmod=algo)

    return hmac_obj.digest()