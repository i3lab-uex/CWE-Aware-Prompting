import hashlib
import hmac

# Secret key used for signing (must be kept confidential)
SECRET_KEY: bytes = b"super_secret_key_please_change"

# List of cryptographic hash algorithms considered secure for HMAC
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
    "sha512_256",  # SHA-512/256 is a truncated version of SHA‑512, still considered secure
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hashing algorithm to use. Must be one of the secure algorithms.
    message : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If an unsupported or insecure hash algorithm is specified.
    """
    # Normalise algorithm name to lower case for comparison
    algo = algorithm.lower()
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm}")

    # Create an HMAC object using the selected digest function
    hmac_obj = hmac.new(SECRET_KEY, message, hashlib.new(algo))
    return hmac_obj.digest()