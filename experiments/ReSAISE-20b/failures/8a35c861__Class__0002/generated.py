import hashlib

# List of cryptographically secure algorithms supported by the standard library.
# Weak or deprecated algorithms (e.g. md5, sha1) are intentionally omitted to avoid CWE‑327.
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha512_224",
    "sha512_256",
    "sm3",            # available on recent Python builds
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    # Extendable‑output functions (SHAKE) are considered secure when used with a
    # fixed output length. They are included for completeness.
    "shake_128",
    "shake_256",
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using a secure algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use. Must be one of SECURE_ALGORITHMS.
    pw : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If algo_name is not in SECURE_ALGORITHMS or the algorithm is unavailable
        in the current hashlib implementation.
    """
    # Normalise name to lower‑case and strip whitespace
    algo = algo_name.strip().lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is not a supported secure hash.")

    try:
        # hashlib.new accepts the algorithm name and returns a new hash object
        hasher = hashlib.new(algo)
    except (AttributeError, ValueError):
        # AttributeError: no 'new' in hashlib; unlikely but guard anyway.
        raise ValueError(f"Hash algorithm '{algo_name}' is not available in this Python build.")

    # Encode the password as UTF‑8 before hashing
    hasher.update(pw.encode("utf-8"))
    return hasher.digest()