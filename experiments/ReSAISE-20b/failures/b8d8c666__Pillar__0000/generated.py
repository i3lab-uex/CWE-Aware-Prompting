import hashlib
import hmac

# A list of hash algorithms that are considered secure for HMAC usage.
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

# Example secret key – in a real application this should be stored securely.
SECRET_KEY = b"my-very-secret-key"


def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hash algorithm to use. Must be one of the allowed secure algorithms.
    payload : bytes
        The raw data to sign.

    Returns
    -------
    bytes
        The computed HMAC signature.

    Raises
    ------
    ValueError
        If the algorithm is unsupported or disallowed.
    """
    if algorithm_name not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name!r}. "
            f"Allowed algorithms are: {sorted(ALLOWED_ALGORITHMS)}"
        )

    # Create a new HMAC object using the selected algorithm.
    h = hmac.new(SECRET_KEY, msg=payload, digestmod=getattr(hashlib, algorithm_name))
    return h.digest()