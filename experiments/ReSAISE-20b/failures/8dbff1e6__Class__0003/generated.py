import hashlib
import hmac

# List of algorithms considered cryptographically secure for HMAC
_SECURE_ALGORITHMS = {
    "sha512_256",
    "sha224",
    "sha384",
    "blake2b",
    "sha3_256",
    "sha256",
    "sm3",          # if supported by the platform
    "sha3_224",
    "shake_128",    # used with a fixed digest size
    "sha512",
    "sha512_224",
    "shake_256",
    "sha3_512",
    "blake2s",
    "sha3_384",
}

# Optional mapping to ensure the algorithm name is accepted by hashlib
_ALGORITHM_MAP = {
    "sha512_256": "sha512_256",
    "sha224": "sha224",
    "sha384": "sha384",
    "blake2b": "blake2b",
    "sha3_256": "sha3_256",
    "sha256": "sha256",
    "sm3": "sm3",          # may raise ValueError if not available
    "sha3_224": "sha3_224",
    "shake_128": "shake_128",
    "sha512": "sha512",
    "sha512_224": "sha512_224",
    "shake_256": "shake_256",
    "sha3_512": "sha3_512",
    "blake2s": "blake2s",
    "sha3_384": "sha3_384",
}

def generate_token(hash_algorithm_name: str, payload: bytes, secret_key: bytes) -> bytes:
    """
    Generate an HMAC signature for the given payload using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm_name : str
        The name of the desired hash algorithm.
    payload : bytes
        The data to be signed.
    secret_key : bytes
        A key used for the HMAC signing procedure.

    Returns
    -------
    bytes
        The generated signature based on the input data.

    Raises
    ------
    ValueError
        If the specified hash algorithm is not supported or considered insecure.
    """
    # Normalise name to lower case
    algo_name = hash_algorithm_name.lower()

    if algo_name not in _SECURE_ALGORITHMS:
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is not supported or considered insecure.")

    # Resolve the actual hashlib name
    try:
        digestmod = _ALGORITHM_MAP[algo_name]
    except KeyError:
        raise ValueError(f"Hash algorithm '{hash_algorithm_name}' is not recognised by hashlib.")

    # For SHAKE algorithms, we need to specify a digest size.
    if algo_name.startswith("shake"):
        # Using 32 bytes (256 bits) as a reasonable default
        digest_size = 32
        hmac_obj = hmac.new(secret_key, msg=payload, digestmod=lambda data: hashlib.shake_128(data).digest(digest_size))
    else:
        hmac_obj = hmac.new(secret_key, msg=payload, digestmod=digestmod)

    return hmac_obj.digest()