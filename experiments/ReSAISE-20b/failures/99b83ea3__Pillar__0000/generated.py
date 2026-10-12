import hashlib
import hmac

# Define a set of secure hash algorithms that are acceptable for HMAC.
SECURE_ALGORITHMS = {
    'sha512_256',
    'sha224',
    'sha384',
    'blake2b',
    'sha3_256',
    'sha256',
    'sm3',          # if supported by the platform
    'sha3_224',
    'shake_128',   # HMAC with variable length output
    'sha512',
    'sha512_224',
    'shake_256',   # HMAC with variable length output
    'sha3_512',
    'blake2s',
    'sha3_384',
}

# Optionally include any other secure algorithms your platform supports.
# Exclude weak ones like md5, sha1, ripemd160, etc.


def create_signature(algorithm_name: str, message: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given message using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256', 'blake2b').
    message : bytes
        The data to be signed.
    secret_key : bytes
        The key used for the HMAC signing procedure.

    Returns
    -------
    bytes
        The computed signature.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalise algorithm name to lower case for comparison
    alg = algorithm_name.lower()

    if alg not in SECURE_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure hash algorithm: {algorithm_name}")

    try:
        # hashlib.new supports most algorithms; if not available, it will raise a ValueError.
        hash_func = hashlib.new(alg)
    except Exception as exc:
        raise ValueError(f"Hash algorithm {algorithm_name} is not available on this platform") from exc

    # Create the HMAC object using the chosen hash function.
    hmac_obj = hmac.new(secret_key, msg=message, digestmod=hash_func)
    return hmac_obj.digest()