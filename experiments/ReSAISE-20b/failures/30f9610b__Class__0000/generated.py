import hashlib
import hmac

# Mapping of supported hash names to their corresponding hashlib constructors.
_SUPPORTED_HASHES = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    "blake2b": hashlib.blake2b,
    "blake2s": hashlib.blake2s,
    "sha3_224": hashlib.sha3_224,
    "sha3_256": hashlib.sha3_256,
    "sha3_384": hashlib.sha3_384,
    "sha3_512": hashlib.sha3_512,
    "shake_128": hashlib.shake_128,
    "shake_256": hashlib.shake_256,
    # Add other names if needed
}

def produce_signature(method_name: str, data: bytes, secret_key: bytes) -> bytes:
    """
    Produce an HMAC signature for the given data using the specified hash algorithm.

    Parameters
    ----------
    method_name : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'md5').
    data : bytes
        The message to be signed.
    secret_key : bytes
        Secret key used for HMAC.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or unavailable.
    """
    # Normalize method name to lower case for a case‑insensitive match
    algo_name = method_name.lower()
    if algo_name not in _SUPPORTED_HASHES:
        raise ValueError(f"Unsupported hash algorithm: {method_name}")

    # Instantiate the hash constructor
    try:
        digestmod = _SUPPORTED_HASHES[algo_name]
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Hash algorithm {method_name} not available") from exc

    # Compute HMAC
    h = hmac.new(secret_key, data, digestmod)
    return h.digest()