import hashlib

# List of weak or deprecated algorithms that should be avoided.
_WEAK_ALGORITHMS = {
    'md5',
    'sha1',
    'ripemd160',
    # Add other known weak algorithms if desired.
}

def calc_hash(hash_name: str, data: bytes) -> bytes:
    """
    Calculate the hash of *data* using the specified *hash_name*.

    Parameters
    ----------
    hash_name : str
        Name of the hash algorithm (e.g. 'sha256', 'md5').
    data : bytes
        The binary data to hash.

    Returns
    -------
    bytes
        The raw digest of the hash function.

    Raises
    ------
    ValueError
        If *hash_name* is not a supported algorithm in hashlib.
    """
    # Normalise the hash name to match what hashlib expects
    norm_name = hash_name.lower()

    # Check if the algorithm is available in this Python build
    try:
        hasher = hashlib.new(norm_name)
    except ValueError as exc:
        raise ValueError(
            f"Hash algorithm '{hash_name}' is not supported in this environment."
        ) from exc

    # Compute the digest
    hasher.update(data)
    digest = hasher.digest()

    # Optionally warn about weak algorithms (CWE‑327)
    if norm_name in _WEAK_ALGORITHMS:
        # In a real application you might log or raise a warning.
        pass  # placeholder: no action taken here

    return digest