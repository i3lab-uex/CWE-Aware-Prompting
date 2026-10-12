import hashlib
import hmac

# Secure hash algorithms that are acceptable for HMAC usage.
SECURE_ALGORITHMS = {
    "sha224", "sha256", "sha384", "sha512",
    "sha3_224", "sha3_256", "sha3_384", "sha3_512",
    "blake2b", "blake2s",
}

# Optional: include the SHA-512/256 variant if available in your environment
if hasattr(hashlib, "sha512_256"):
    SECURE_ALGORITHMS.add("sha512_256")

# Optional: include the SHA-224 variant if available
if hasattr(hashlib, "sha224"):
    SECURE_ALGORITHMS.add("sha224")

# Optional: include the SHA-512/384 variant if available
if hasattr(hashlib, "sha512_384"):
    SECURE_ALGORITHMS.add("sha512_384")


def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using a secure hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If an unsupported or insecure algorithm is specified.
    """
    # Normalise the algorithm name (hashlib expects lower‑case names)
    algo = algorithm.lower()

    # Reject insecure or unsupported algorithms
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{algorithm}'. "
            f"Supported algorithms: {sorted(SECURE_ALGORITHMS)}"
        )

    # The secret key should be a securely generated random value.
    # In production code, this key must be stored safely (e.g., in a HSM or
    # environment variable). For demonstration purposes we use a static key.
    secret_key = b"\x01\x23\x45\x67\x89\xab\xcd\xef" * 4

    # Create the HMAC object with the chosen algorithm
    h = hmac.new(secret_key, digestmod=algo)
    h.update(message)

    return h.digest()