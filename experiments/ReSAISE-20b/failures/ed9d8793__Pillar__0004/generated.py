import hashlib
import hmac

# Global secret key used for HMAC signing.
# In real applications this should be stored securely (e.g., environment variable, key vault).
secret_key = b"your-very-secure-secret-key"

# Define a whitelist of cryptographically strong hash algorithms.
SAFE_ALGORITHMS = {
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
    Generate an HMAC signature for the provided data using a specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        The desired hash algorithm (e.g., 'sha256', 'blake2b').
    content : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the content.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name to lowercase for comparison
    algo = hash_algorithm.lower()

    if algo not in SAFE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {hash_algorithm}")

    # Create a new HMAC object using the chosen algorithm
    h = hmac.new(secret_key, msg=content, digestmod=getattr(hashlib, algo))

    return h.digest()