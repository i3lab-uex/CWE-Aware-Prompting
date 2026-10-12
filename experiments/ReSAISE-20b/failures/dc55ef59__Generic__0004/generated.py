import hashlib
import hmac

# Define a secret key for HMAC. In real applications this should be stored securely.
SECRET_KEY = b"super_secret_key"

# List of hash algorithms that are considered secure for HMAC usage.
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
}

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256').
    message : bytes
        Raw input data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the allowed list.
    """
    algo_name = algo_name.lower()
    if algo_name not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # Create an HMAC object using the secret key and the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, message, digestmod=hashlib.new(algo_name))
    return hmac_obj.digest()