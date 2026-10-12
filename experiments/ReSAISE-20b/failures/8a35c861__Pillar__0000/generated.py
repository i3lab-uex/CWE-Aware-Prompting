import hashlib

# List of cryptographic algorithms considered secure for hashing passwords.
SECURE_ALGORITHMS = {
    'sha224',
    'sha256',
    'sha384',
    'sha512',
    'sha512_224',
    'sha512_256',
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'blake2b',
    'blake2s',
}

def secure_hash(algo_name: str, pw: str) -> bytes:
    """
    Compute a cryptographic hash of the supplied password using the requested algorithm.

    Parameters
    ----------
    algo_name : str
        The name of the hash algorithm to use. Must be one of the secure algorithms listed in SECURE_ALGORITHMS.
    pw : str
        The password to hash.

    Returns
    -------
    bytes
        The raw digest of the password.

    Raises
    ------
    ValueError
        If the requested algorithm is not available in the current Python installation or is considered insecure.
    """
    # Normalise algorithm name
    algo = algo_name.lower()

    # Check that the requested algorithm is in our whitelist of secure algorithms
    if algo not in SECURE_ALGORITHMS:
        raise ValueError(f"Algorithm '{algo_name}' is not supported or considered insecure.")

    # Ensure the algorithm is actually available in hashlib
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm '{algo_name}' is not available on this system.")

    # Create the hash object and feed it the password bytes
    h = hashlib.new(algo)
    h.update(pw.encode('utf-8'))

    # Return the raw digest bytes
    return h.digest()