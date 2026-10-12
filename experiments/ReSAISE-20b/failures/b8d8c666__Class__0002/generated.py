import hashlib
import hmac

# The secret key used for HMAC.  It should be a securely generated random
# byte string of sufficient length (e.g., 32 bytes for SHA‑256/384/512).
# In a real application this would be stored securely (e.g., in a key
# management system) and not hard‑coded.
secret_key: bytes = b'\x01\x02\x03\x04'  # placeholder – replace with real key

# A set of hash algorithms that are considered secure for HMAC usage.
ALLOWED_ALGORITHMS = {
    'sha256', 'sha384', 'sha512',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    # The following are also widely regarded as secure and
    # provide additional options for users:
    'blake2b', 'blake2s',
}

def create_signature(algorithm_name: str, payload: bytes) -> bytes:
    """
    Create an HMAC signature of the given payload using the specified hash
    algorithm.

    Parameters
    ----------
    algorithm_name : str
        The name of the hash algorithm to use (e.g., 'sha256').
    payload : bytes
        The data to be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If the supplied algorithm is not in the list of allowed algorithms.
    """
    # Normalise the algorithm name (case‑insensitive)
    alg = algorithm_name.lower()

    if alg not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {algorithm_name}"
        )

    # Create the HMAC object using the chosen algorithm
    hmac_obj = hmac.new(secret_key, payload, digestmod=alg)

    return hmac_obj.digest()