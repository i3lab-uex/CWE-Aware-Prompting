import hashlib
import hmac

# Secret key used for the HMAC signature (must be kept confidential).
# In a real application this would come from secure storage or an environment variable.
secret_key: bytes = b"super_secret_key"

# Set of cryptographic hash algorithms that are considered secure for HMAC.
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

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature of the given message using a secure hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    message : bytes
        The raw input data that will be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the list of allowed secure algorithms.
    """
    # Normalise algorithm name to lowercase to avoid case‑sensitivity issues
    algo_name = algo_name.lower()

    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # Construct the HMAC object with the chosen digest method.
    hmac_obj = hmac.new(secret_key, message, digestmod=algo_name)
    return hmac_obj.digest()