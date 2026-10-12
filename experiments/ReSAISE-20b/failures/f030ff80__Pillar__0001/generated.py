import hashlib

def secure_password_hash(hash_type: str, pass_input: str) -> str:
    """
    Hash a password using the specified algorithm and return its hexadecimal digest.

    Args:
        hash_type (str): Name of a supported hashlib algorithm.
        pass_input (str): The plaintext password to hash.

    Returns:
        str: Hexadecimal representation of the hashed password.

    Raises:
        ValueError: If `hash_type` is not a supported algorithm.
    """
    # Ensure the requested hash type exists in hashlib's available algorithms
    if hash_type.lower() not in {alg.lower() for alg in hashlib.algorithms_available}:
        raise ValueError(f"Unsupported hash algorithm: '{hash_type}'. "
                         f"Supported algorithms include: {sorted(hashlib.algorithms_available)}")

    # Create a new hash object
    hasher = hashlib.new(hash_type)

    # Encode the password to bytes and update the hash
    hasher.update(pass_input.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()