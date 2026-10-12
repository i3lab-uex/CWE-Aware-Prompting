import hmac
import hashlib

# A set of cryptographically secure hashing algorithms.
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
    # sm3 is considered secure in some contexts, but it may not be available on all platforms.
    "sm3",
}

def create_checksum(
    algorithm_name: str,
    message_data: bytes,
    secret_key: bytes
) -> bytes:
    """
    Generate a cryptographic HMAC signature for the supplied message data.

    Parameters
    ----------
    algorithm_name : str
        The name of a secure hashing algorithm to use (e.g. 'sha256', 'blake2b').
    message_data : bytes
        The raw data that needs to be signed.
    secret_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the supplied algorithm is not in the list of secure algorithms.
    """
    # Normalise the algorithm name to lower case because hashlib accepts
    # case‑insensitive names but we want a deterministic set.
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: {algorithm_name!r}. "
            "Supported algorithms are: " + ", ".join(sorted(SECURE_ALGORITHMS))
        )

    # Resolve the hash constructor from hashlib
    try:
        digestmod = getattr(hashlib, algo)
    except AttributeError as exc:
        # This should never happen because we checked the set, but guard anyway.
        raise ValueError(f"Hash algorithm {algorithm_name!r} is not available.") from exc

    # Create the HMAC object and return its digest.
    hmac_obj = hmac.new(secret_key, message_data, digestmod)
    return hmac_obj.digest()