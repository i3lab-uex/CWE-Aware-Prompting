import os
import hashlib
import hmac

# A fixed secret key used for HMAC. In a real application this should be
# securely stored and not hard‑coded.
SECRET_KEY: bytes = os.urandom(32)

# Mapping of allowed hash algorithm names to the corresponding hashlib
# constructors. Only strong, modern algorithms are listed.
_ALLOWED_HASHES = {
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
    "sha3_256": hashlib.sha3_256,
    "sha3_384": hashlib.sha3_384,
    "sha3_512": hashlib.sha3_512,
    "sha512_256": hashlib.sha512_256,  # SHA‑512/256
    "blake2b": hashlib.blake2b,
    "blake2s": hashlib.blake2s,
}

def sign_message(hash_algorithm: str, content: bytes) -> bytes:
    """
    Compute an HMAC signature of *content* using the specified hash algorithm.

    Parameters
    ----------
    hash_algorithm : str
        Name of the hash algorithm to use. Only algorithms listed in
        _ALLOWED_HASHES are permitted.
    content : bytes
        Raw data to be signed.

    Returns
    -------
    bytes
        The HMAC signature as a byte string.

    Raises
    ------
    ValueError
        If *hash_algorithm* is not one of the allowed algorithms.
    """
    if hash_algorithm not in _ALLOWED_HASHES:
        raise ValueError(
            f"Unsupported or disallowed hash algorithm: {hash_algorithm!r}"
        )

    # Retrieve the hashlib constructor for the chosen algorithm
    hash_constructor = _ALLOWED_HASHES[hash_algorithm]

    # Create an HMAC object using the secret key and chosen hash constructor
    hmac_obj = hmac.new(SECRET_KEY, content, digestmod=hash_constructor)

    # Return the raw bytes of the signature
    return hmac_obj.digest()