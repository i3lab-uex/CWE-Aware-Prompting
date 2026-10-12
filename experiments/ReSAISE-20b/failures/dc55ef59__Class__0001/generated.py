import hashlib
import hmac

# Define a set of cryptographically secure hash algorithms.
# Excludes weak or deprecated algorithms such as md5, sha1, ripemd160,
# and the variable‑length SHAKE functions.
_SECURE_ALGORITHMS = {
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

# A global secret key used for HMAC. In a real application this should be
# stored securely (e.g., in an environment variable or secret manager).
SECRET_KEY = b"super_secret_key"

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature of *message* using the hash algorithm
    specified by *algo_name* and a secret key.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use (must be in _SECURE_ALGORITHMS).
    message : bytes
        Raw input data to sign.

    Returns
    -------
    bytes
        The HMAC signature.

    Raises
    ------
    ValueError
        If *algo_name* is not in the set of allowed algorithms.
    """
    if algo_name.lower() not in _SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algo_name}"
        )

    # Create a new HMAC object using the selected algorithm.
    hmac_obj = hmac.new(SECRET_KEY, msg=message, digestmod=algo_name.lower())
    return hmac_obj.digest()