import hashlib
import hmac

# Secret key used for HMAC signing (must be kept confidential)
SECRET_KEY: bytes = b"your-very-secret-key-here"

# Set of hash algorithms considered secure for HMAC usage
SECURE_HASHES = {
    "sha256",
    "sha384",
    "sha512",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
}

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Create an HMAC signature of *content* using the specified *hash_algorithm*.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use (e.g., 'sha256').
    content : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The HMAC digest of the content.

    Raises
    ------
    ValueError
        If *hash_algorithm* is not in the list of permitted algorithms.
    """
    # Normalise algorithm name to lower case
    algo = hash_algorithm.lower()

    if algo not in SECURE_HASHES:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {hash_algorithm!r}"
        )

    # Create the HMAC object with the chosen hash function
    try:
        digestmod = getattr(hashlib, algo)
    except AttributeError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm {hash_algorithm!r} is not available") from exc

    hmac_obj = hmac.new(SECRET_KEY, content, digestmod)
    return hmac_obj.digest()