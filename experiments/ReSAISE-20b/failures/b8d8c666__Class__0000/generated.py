import hashlib
import hmac

# Define a whitelist of cryptographically strong hash algorithms.
# Weak or deprecated algorithms (md5, sha1, ripemd160, etc.) are excluded.
_ALLOWED_HASH_ALGORITHMS = {
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

# Example secret key for HMAC. In real applications this should be kept secure.
SECRET_KEY = b"super_secret_key"

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature for the given payload using a secure hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        Raw input data to be signed.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the whitelist of secure algorithms.
    """
    # Normalise the algorithm name to lower case and strip whitespace
    algo = algorithm_name.strip().lower()

    if algo not in _ALLOWED_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name!r}. "
            "Allowed algorithms are: " + ", ".join(sorted(_ALLOWED_HASH_ALGORITHMS))
        )

    # Create an HMAC object with the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, payload, digestmod=algo)
    return hmac_obj.digest()