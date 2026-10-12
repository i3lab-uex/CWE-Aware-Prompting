import hashlib

# A set of algorithms considered cryptographically strong for this context.
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'sha512_224',
    'sha512',
    'sm3',          # SM3 is accepted in some environments
    'sha3_384',
    'shake_128',    # SHAKE algorithms are XOFs but still secure
    'sha256',
    'blake2b',
    'md5-sha1',     # a combined hash that is not widely used but available
    'shake_256',
    'ripemd160',    # considered secure in many contexts
    'sha3_256',
    'blake2s',
    'sha3_512',
    'sha3_224'
}

# Algorithms that are known to be weak or broken and should not be used.
WEAK_ALGORITHMS = {'md5', 'sha1'}


def generate_hash(algo_hash: str, pwd_input: str) -> bytes:
    """
    Generate a cryptographic hash of the given password using the specified algorithm.

    Parameters
    ----------
    algo_hash : str
        The name of the cryptographic algorithm to use.
    pwd_input : str
        The password string to hash.

    Returns
    -------
    bytes
        The raw digest of the hashed password.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported, not available in hashlib,
        or considered insecure.
    """
    # Normalize the algorithm name to lower case for comparison
    algo = algo_hash.lower()

    if algo in WEAK_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is considered insecure and cannot be used.")

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_hash}' is not recognized as a supported secure algorithm.")

    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_hash}' is not available on this system.")

    # Create the hash object and feed it the password bytes
    hasher = hashlib.new(algo)
    hasher.update(pwd_input.encode('utf-8'))
    return hasher.digest()