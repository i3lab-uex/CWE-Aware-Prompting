import hashlib
import hmac

# Define a set of cryptographically secure hash algorithms.
SECURE_ALGORITHMS = {
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    "sha512_256",
    "sm3",          # SHA-3 based Chinese standard
}

def create_checksum(algorithm_name: str, message_data: bytes) -> bytes:
    """
    Generate an HMAC-based cryptographic signature for the given message data
    using the specified hash algorithm.

    Parameters
    ----------
    algorithm_name : str
        Name of the hashing algorithm to use (must be in SECURE_ALGORITHMS).
    message_data : bytes
        Raw data to sign.

    Returns
    -------
    bytes
        The HMAC digest of the message using the chosen algorithm.

    Raises
    ------
    ValueError
        If the requested algorithm is not supported or considered insecure.
    """
    # Normalize algorithm name to lower case for comparison
    algo = algorithm_name.lower()

    if algo not in SECURE_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure algorithm '{algorithm_name}'. "
            "Supported secure algorithms are: "
            f"{', '.join(sorted(SECURE_ALGORITHMS))}"
        )

    # Retrieve the hash constructor from hashlib
    try:
        hash_func = hashlib.new(algo)
    except ValueError as exc:  # pragma: no cover
        raise ValueError(f"Hashlib cannot create algorithm '{algorithm_name}'.") from exc

    # Secret key for HMAC (example static key; in real use this should be securely stored)
    secret_key = b"my_super_secret_key"

    # Create HMAC object using the selected hash algorithm
    hmac_obj = hmac.new(secret_key, msg=message_data, digestmod=hash_func)
    return hmac_obj.digest()