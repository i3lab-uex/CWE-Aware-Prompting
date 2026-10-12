import hashlib
import hmac

# Secret key used for HMAC.  In a real application this should be stored securely.
SECRET_KEY: bytes = b"super_secret_key"

# Define the set of hash algorithms that are considered secure.
ALLOWED_ALGORITHMS = {
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
}

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature for *message* using the hash algorithm *algo_name*.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g. 'sha256', 'blake2b').
    message : bytes
        Raw input data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If *algo_name* is not in the set of allowed algorithms.
    """
    algo_name_lower = algo_name.lower()
    if algo_name_lower not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # Create the HMAC object using the chosen algorithm.
    h = hmac.new(SECRET_KEY, digestmod=hashlib.new(algo_name_lower))
    h.update(message)
    return h.digest()