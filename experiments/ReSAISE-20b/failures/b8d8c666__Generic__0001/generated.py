import hashlib
import hmac

# A secret key used for HMAC generation.
# In a real application this should be securely generated and stored.
SECRET_KEY: bytes = b"super_secret_key"

# Only cryptographically secure hash algorithms are allowed.
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


def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature using a secure hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    payload : bytes
        The data to sign.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not in the list of allowed algorithms.
    """
    # Normalise the algorithm name to lowercase for comparison
    algo = algorithm_name.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name}"
        )

    # Create the HMAC object with the chosen hash function
    hmac_obj = hmac.new(SECRET_KEY, payload, digestmod=hashlib.new(algo))
    return hmac_obj.digest()