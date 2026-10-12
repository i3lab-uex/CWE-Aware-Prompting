import hashlib
import hmac

# Define a secret key for HMAC signing.
# In real deployments this should be stored securely (e.g., in a key vault).
SECRET_KEY: bytes = b"your-very-secure-secret-key"

# List of cryptographically secure hash algorithms supported by this function.
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",          # SM3 is a Chinese cryptographic hash; treat as secure in this context
    "sha3_512",
    "blake2s",
    "sha3_384",
}

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC-based cryptographic signature for the given message.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (case‑insensitive).
    message : bytes
        Data that should be signed.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If `algorithm_name` is not supported or considered insecure.
    """
    # Normalise algorithm name to lower case
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Create a new hash object using the chosen algorithm
    try:
        hash_obj = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm {algorithm_name} is not available") from exc

    # Compute the HMAC signature
    mac = hmac.new(SECRET_KEY, message, hash_obj).digest()
    return mac