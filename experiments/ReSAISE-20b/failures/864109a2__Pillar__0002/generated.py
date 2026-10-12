import hashlib

def encode_password(hash_algorithm: str, plain_text_pwd: str) -> str:
    """
    Hashes a plaintext password using the specified hash algorithm and returns
    its hexadecimal representation.

    Parameters:
        hash_algorithm (str): Name of the hash algorithm to use.
        plain_text_pwd (str): The plaintext password.

    Returns:
        str: Hexadecimal string of the hashed password.

    Raises:
        ValueError: If the specified hash algorithm is not supported or
                    unavailable in the current environment.
    """
    # Normalize algorithm name to lower case for consistency with hashlib
    algo_name = hash_algorithm.lower()

    # Check if the algorithm is available in this Python environment
    if algo_name not in hashlib.algorithms_available:
        raise ValueError(
            f"Unsupported or unavailable hash algorithm: '{hash_algorithm}'. "
            "Please choose one of the following supported algorithms: "
            f"{', '.join(sorted(hashlib.algorithms_available))}"
        )

    # Create a new hash object and update it with the password bytes
    hasher = hashlib.new(algo_name)
    # Ensure the input is encoded to bytes; UTF-8 is a common safe choice
    hasher.update(plain_text_pwd.encode('utf-8'))

    # Return the hexadecimal digest
    return hasher.hexdigest()