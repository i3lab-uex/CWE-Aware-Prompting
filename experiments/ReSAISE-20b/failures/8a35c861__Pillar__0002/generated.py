import hashlib

# A curated set of cryptographic hash algorithms considered secure for password hashing.
# Weak algorithms such as MD5 and SHA‑1 are deliberately omitted to avoid CWE‑693 vulnerabilities.
SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "sha512_224",
    "sha512",
    "sm3",
    "sha3_384",
    "shake_128",   # used with a fixed digest size
    "sha256",
    "blake2b",
    "shake_256",   # used with a fixed digest size
    "ripemd160",
    "sha3_256",
    "blake2s",
    "sha3_512",
    "sha3_224",
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm (e.g. 'sha256', 'blake2b').
    pw : str
        Password to hash.

    Returns
    -------
    bytes
        The raw digest bytes of the password.

    Raises
    ------
    ValueError
        If `algo_name` is not in the list of supported secure algorithms,
        or if the algorithm is unavailable on this platform.
    """
    # Normalise and validate the algorithm name
    algo_name = algo_name.lower()
    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure algorithm: {algo_name}")

    try:
        # `hashlib.new` will raise a ValueError if the algorithm is not available
        hasher = hashlib.new(algo_name)
    except ValueError as exc:
        raise ValueError(f"Algorithm '{algo_name}' is not available on this system") from exc

    # Encode the password as UTF‑8 before hashing
    hasher.update(pw.encode("utf-8"))
    return hasher.digest()