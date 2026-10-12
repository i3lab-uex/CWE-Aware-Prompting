import hmac
import hashlib

# A global secret key used for HMAC signing.
# In a real application this should be stored securely (e.g., in an environment variable or a key‑management service).
secret_key = b"your-very-secret-key"

# Set of algorithms considered secure for HMAC usage.
SECURE_ALGORITHMS = {
    "sha512_256", "sha224", "sha384", "blake2b",
    "sha3_256", "sha256", "sm3", "sha3_224",
    "shake_128", "sha512", "sha512_224",
    "shake_256", "sha3_512", "blake2s",
    "sha3_384", "ripemd160"
}

def create_signature(algorithm_name: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the desired hash algorithm (e.g., "sha256").
    message : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name to lower case (hashlib accepts this form).
    algo = algorithm_name.lower()

    # Ensure the requested algorithm is supported and secure.
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    # Create the HMAC object using the chosen digest.
    try:
        digest_mod = hashlib.new(algo)
    except ValueError as exc:
        # This should not happen because we validated the algorithm name,
        # but we guard against any unexpected hashlib behaviour.
        raise ValueError(f"Hash algorithm '{algorithm_name}' is not available") from exc

    h = hmac.new(secret_key, message, digestmod=digest_mod)
    return h.digest()