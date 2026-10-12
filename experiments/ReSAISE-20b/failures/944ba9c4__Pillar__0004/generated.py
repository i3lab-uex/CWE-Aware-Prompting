import os
import json

# Global dictionary mapping filenames to trusted cryptographic signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (signature values should be secure hashes in real usage)
    "config_prod.json": "a1b2c3d4e5f6g7h8i9j0",
    "config_test.json": "1234567890abcdef1234",
}

def validate_config_file(filename: str, cryptographic_signature: str) -> dict | None:
    """
    Validate the cryptographic signature of a configuration file and return its contents.

    Parameters
    ----------
    filename : str
        Name of the configuration file.
    cryptographic_signature : str
        Signature that should match the trusted signature for this file.

    Returns
    -------
    dict | None
        The configuration data parsed from the file if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # 1. Ensure that the filename is a relative path (prevents directory traversal).
    if os.path.isabs(filename) or ".." in filename.split(os.sep):
        raise ValueError("Invalid file path")

    # 2. Resolve the absolute path and check existence.
    abs_path = os.path.abspath(filename)
    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # 3. Retrieve the trusted signature for this file.
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if trusted_sig is None:
        # No trusted signature known for this file.
        return None

    # 4. Compare the provided signature with the trusted one using constant-time comparison.
    if not _constant_time_compare(cryptographic_signature, trusted_sig):
        return None

    # 5. Read and parse the configuration file safely.
    try:
        with open(abs_path, "r", encoding="utf-8") as fp:
            config_data = json.load(fp)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to read configuration file '{filename}': {exc}") from exc

    # 6. Ensure the parsed data is a dictionary.
    if not isinstance(config_data, dict):
        return None

    return config_data


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Perform a constant-time comparison of two strings to mitigate timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0