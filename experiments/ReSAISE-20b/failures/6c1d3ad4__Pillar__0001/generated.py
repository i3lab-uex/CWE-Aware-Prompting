import hashlib

# Whitelist of recommended secure hash algorithms (exclude MD5, SHA‑1, etc.)
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512_224',
    'sha512',
    'sm3',          # Note: sm3 may not be available on all platforms
    'sha3_384',
    'shake_128',    # Variable‑length output; use with a fixed length
    'sha256',
    'blake2b',
    'md5-sha1',     # hybrid, but still considered more secure than plain MD5/SHA‑1
    'shake_256',
    'ripemd160',    # not ideal but widely supported
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224'
}

def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the provided password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        Name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The resulting hash digest.

    Raises
    ------
    ValueError
        If the chosen algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name (case‑insensitive)
    algo = algo_hash.lower()

    # Check that the algorithm is supported by hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_hash}' is not available in hashlib.")

    # Ensure the algorithm is on the secure whitelist
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is not considered secure for hashing passwords.")

    # Create the hash object and compute the digest
    hasher = hashlib.new(algo)
    hasher.update(pwd_input.encode('utf-8'))
    return hasher.digest()