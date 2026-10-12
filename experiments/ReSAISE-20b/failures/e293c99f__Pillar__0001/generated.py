import hmac
import hashlib

# A secret key used for HMAC. In a real application this should be stored
# securely (e.g., in an environment variable or a secrets manager) and never
# hard‑coded. For demonstration purposes it is defined here as a constant.
secret_key: bytes = b"super_secret_key"

# Set of cryptographic hash algorithms that are considered secure for HMAC.
# Algorithms such as MD5, SHA1, and the extendable‑output functions (shake)
# are excluded because they have known weaknesses or are not intended for
# HMAC usage.
_SECURE_HASH_ALGORITHMS = {
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
}

def create_signature(algo_name: str, raw_data: bytes) -> bytes:
    """
    Generate an HMAC signature for the given data using a secure hash algorithm.

    Parameters
    ----------
    algo_name : str
        Name of the hashing algorithm to use (e.g., 'sha256', 'blake2b').
    raw_data : bytes
        The raw data that needs to be signed.

    Returns
    -------
    bytes
        The HMAC signature for the provided data.

    Raises
    ------
    ValueError
        If an unsupported or insecure hash algorithm is specified.
    """
    algo_name_lower = algo_name.lower()
    if algo_name_lower not in _SECURE_HASH_ALGORITHMS:
        raise ValueError(
            f"Unsupported or insecure hash algorithm: '{algo_name}'. "
            "Allowed algorithms are: "
            f"{', '.join(sorted(_SECURE_HASH_ALGORITHMS))}"
        )

    # HMAC requires a hash constructor. The `hashlib.new` function accepts the
    # algorithm name and returns a new hash object. We pass that constructor to
    # `hmac.new` so that the HMAC uses the desired algorithm.
    hash_constructor = hashlib.new(algo_name_lower)
    hmac_obj = hmac.new(secret_key, raw_data, digestmod=hash_constructor)
    return hmac_obj.digest()