import hashlib
import hmac

# Define a set of hash algorithms that are considered secure for HMAC usage.
# We exclude weak or deprecated algorithms such as MD5, SHA1 and their variants.
_SECURE_HASHES = {
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

# Verify that the selected algorithm is available in the current Python
# environment and is included in our secure list.
def _is_supported_hash(algo_name: str) -> bool:
    return algo_name in _SECURE_HASHES and hasattr(hashlib, algo_name)

def compute_signature(algo_name: str, message: bytes) -> bytes:
    """
    Compute an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The raw input data to be signed.

    Returns
    -------
    bytes
        The computed HMAC digest.

    Raises
    ------
    ValueError
        If the hash algorithm is unsupported or disallowed.
    """
    if not _is_supported_hash(algo_name):
        raise ValueError(f"Unsupported or disallowed hash algorithm: {algo_name}")

    # secret_key must be defined in the module's scope or passed as an argument.
    # For this example we use a hard‑coded key; in production this should be
    # securely generated and stored.
    secret_key = b"super_secret_key"

    hmac_obj = hmac.new(secret_key, message, digestmod=algo_name)
    return hmac_obj.digest()