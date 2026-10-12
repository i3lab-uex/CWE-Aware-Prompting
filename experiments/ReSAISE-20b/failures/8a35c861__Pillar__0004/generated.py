import hashlib

# Define a whitelist of cryptographically secure algorithms.
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512_224',
    'sha512',
    'sm3',           # cryptographic hash used in Chinese standards
    'sha3_384',
    'sha256',
    'blake2b',
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224',
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Hash a password using the specified algorithm from a secure whitelist.

    Parameters
    ----------
    algo_name : str
        Name of the hash algorithm to use.
    pw : str
        The password string to be hashed.

    Returns
    -------
    bytes
        Digest of the hash function applied to the password.

    Raises
    ------
    ValueError
        If ``algo_name`` is not in the whitelist of secure algorithms.
    """
    # Normalise algorithm name (hashlib uses lower case names)
    algo_name = algo_name.lower()

    if algo_name not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is not allowed or not secure.")

    # Create a new hash object
    hasher = hashlib.new(algo_name)

    # Encode password to bytes (UTF‑8 is standard for text hashing)
    hasher.update(pw.encode('utf-8'))

    # Return the digest bytes
    return hasher.digest()