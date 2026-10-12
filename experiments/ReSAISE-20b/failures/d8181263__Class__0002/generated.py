import hashlib
import hmac

# Define a secret key to be used for signing.
# In real applications this should come from a secure source
# (e.g., environment variable, key management system).
SECRET_KEY: bytes = b"your-very-secure-secret-key"

# List of cryptographically secure hash algorithms supported by hashlib.
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

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        Raw data that needs to be signed.

    Returns
    -------
    bytes
        The generated HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalise the algorithm name (hashlib accepts lower‑case names).
    algo = algorithm.lower()

    # Ensure the chosen algorithm is in our whitelist.
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm '{algorithm}'. "
            f"Supported algorithms: {', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Create the HMAC object using the chosen hash algorithm.
    try:
        h = hmac.new(SECRET_KEY, msg=message, digestmod=getattr(hashlib, algo))
    except AttributeError as exc:
        # This should never happen because we already validated the algorithm,
        # but guard against accidental misuse.
        raise ValueError(f"Hashlib does not support algorithm '{algorithm}'.") from exc

    return h.digest()