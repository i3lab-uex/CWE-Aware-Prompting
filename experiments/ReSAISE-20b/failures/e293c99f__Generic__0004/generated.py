import hashlib
import hmac

# ------------------------------------------------------------------
# NOTE:  The secret key used for HMAC signing must be kept confidential
# and preferably derived from a secure source (e.g., environment
# variable, key‑management service).  The following is a placeholder.
# ------------------------------------------------------------------
secret_key: bytes = b"your-very-secret-key"

# List of hash algorithms that are considered secure for signing.
SECURE_ALGORITHMS = {
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
    "sm3",           # Supported by OpenSSL 1.1.1+; treat as secure
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC signature for `raw_data` using the specified
    cryptographic hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm (e.g., 'sha256', 'blake2b').
    raw_data : bytes
        The data to be signed.

    Returns
    -------
    bytes
        HMAC signature of the data.

    Raises
    ------
    ValueError
        If `algo_name` is not a supported or secure algorithm.
    """
    # Normalise the algorithm name (case‑insensitive)
    algo_name = algo_name.lower()

    # Validate that the algorithm is both available and considered secure
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algo_name}")

    if algo_name not in hashlib.algorithms_available:
        raise ValueError(f"Hash algorithm '{algo_name}' is not available on this system")

    # Create the HMAC object using the chosen hash function
    hmac_obj = hmac.new(secret_key, raw_data, digestmod=hashlib.new(algo_name))
    return hmac_obj.digest()