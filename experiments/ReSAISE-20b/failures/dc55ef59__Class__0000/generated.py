import hashlib
import hmac

# A hard‑coded secret key for HMAC.  In a real system this should be
# securely generated and stored (e.g., via environment variables or a key
# management service).  For the purpose of this example we keep it simple.
SECRET_KEY: bytes = b'supersecret-key-please-change'

# Define the set of cryptographically secure hash algorithms that are
# allowed for use.  This explicitly excludes weak or broken algorithms
# such as MD5, SHA‑1 and others.
ALLOWED_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
}

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature of *message* using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The raw data to sign.

    Returns
    -------
    bytes
        The resulting HMAC signature.

    Raises
    ------
    ValueError
        If *algo_name* is not in the list of allowed algorithms.
    """
    # Normalise algorithm name to lowercase for comparison
    algo = algo_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # Create the HMAC object using the chosen digest method
    hmac_obj = hmac.new(SECRET_KEY, message, digestmod=getattr(hashlib, algo))
    return hmac_obj.digest()