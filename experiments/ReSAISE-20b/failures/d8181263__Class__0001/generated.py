import hashlib
import hmac

# A secret key that must be kept confidential. In a real system this would
# come from a secure store or environment variable, not hard‑coded.
SECRET_KEY = b'\x01\x23\x45\x67\x89\xab\xcd\xef'  # example key, replace with real one

# Hash algorithms that are considered secure for HMAC usage.
ALLOWED_ALGORITHMS = {
    'sha256',
    'sha384',
    'sha512',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
    'sha224',
    'sha512_256',
}

def sign_data(algorithm: str, message: bytes) -> bytes:
    """
    Generate an HMAC signature for *message* using the specified hash *algorithm*.

    Parameters
    ----------
    algorithm : str
        Name of a cryptographic hash algorithm supported by hashlib.
    message : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The HMAC signature of the message.

    Raises
    ------
    ValueError
        If *algorithm* is not in the list of allowed (secure) algorithms.
    """
    # Normalise algorithm name to avoid case‑sensitivity issues
    algo = algorithm.lower()

    if algo not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm!r}. "
            f"Allowed algorithms are: {sorted(ALLOWED_ALGORITHMS)}"
        )

    # Create a new hash object for the chosen algorithm
    try:
        hash_obj = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hashlib cannot create algorithm {algorithm!r}") from exc

    # Compute HMAC using the secure hash function
    signature = hmac.new(SECRET_KEY, message, digestmod=hash_obj).digest()
    return signature