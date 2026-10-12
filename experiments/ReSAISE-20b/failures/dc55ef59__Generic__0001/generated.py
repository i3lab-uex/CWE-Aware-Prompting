import hashlib
import hmac

# Secret key used for HMAC signing (should be kept confidential)
secret_key: bytes = b"YOUR_SECRET_KEY_HERE"

# Set of cryptographically secure hash algorithms allowed for signing
ALLOWED_ALGORITHMS = {
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
}

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC-based cryptographic signature for the given message
    using a secure hash algorithm.

    Parameters:
        algo_name (str): Name of the hash algorithm to use.
        message (bytes): Raw input data to be signed.

    Returns:
        bytes: The computed HMAC signature.

    Raises:
        ValueError: If the provided algorithm is not supported or disallowed.
    """
    # Normalise the algorithm name to lower case
    algo = algo_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # Create a new hash object for the chosen algorithm
    try:
        hasher = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm '{algo_name}' is not available.") from exc

    # Compute HMAC using the secret key and the chosen hash algorithm
    hmac_obj = hmac.new(secret_key, message, hasher)
    return hmac_obj.digest()