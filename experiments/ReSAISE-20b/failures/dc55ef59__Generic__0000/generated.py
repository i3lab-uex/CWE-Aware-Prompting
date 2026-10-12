import hashlib
import hmac

# Define the list of hash algorithms that are considered secure.
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
    "sha512_256",
    "sm3",      # if supported by the underlying OpenSSL
}

# Secret key used for HMAC (in a real application this should be stored securely).
SECRET_KEY = b"super-secret-key"

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature of *message* using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the algorithm name is not in the list of allowed (secure) algorithms.
    """
    # Normalise the algorithm name
    algo_name = algo_name.lower()

    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # Create a new hash object using the requested algorithm
    try:
        hasher = hashlib.new(algo_name)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm {algo_name} is not available") from exc

    # Compute the HMAC using the secret key
    hmac_obj = hmac.new(SECRET_KEY, message, hasher)
    return hmac_obj.digest()