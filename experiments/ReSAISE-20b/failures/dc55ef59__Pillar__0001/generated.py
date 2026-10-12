import hashlib
import hmac

# NOTE: In a real application the secret key should be stored securely,
# e.g. in an environment variable or a dedicated secrets manager.
# For demonstration purposes we hard‑code it here as a placeholder.
SECRET_KEY: bytes = b"my_very_secret_key"

# A whitelist of cryptographically strong hash algorithms.
# The list intentionally excludes weak or deprecated algorithms such as
# md5, sha1, and the SHA-2 family variants that are no longer recommended.
ALLOWED_ALGORITHMS = {
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
    "sha512_256",
    # If your platform supports SM3 or other algorithms, add them here
}

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature of *message* using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use. Must be in ``ALLOWED_ALGORITHMS``.
    message : bytes
        The raw input data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If *algo_name* is not supported or disallowed.
    """
    # Normalise the algorithm name (hashlib accepts lower‑case names)
    algo_name = algo_name.lower()

    # Ensure the algorithm is available on this platform
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available on this system.")

    # Ensure the algorithm is in our whitelist of secure algorithms
    if algo_name not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{algo_name}' is disallowed for security reasons.")

    # Create an HMAC object using the chosen digest algorithm
    hmac_obj = hmac.new(SECRET_KEY, message, digestmod=algo_name)

    # Return the raw bytes of the HMAC signature
    return hmac_obj.digest()