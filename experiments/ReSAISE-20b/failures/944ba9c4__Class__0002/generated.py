import json
import hmac
import os

# Global dictionary mapping filenames to their expected cryptographic signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "config.yaml": "a1b2c3d4e5f6g7h8i9j0",
    # "settings.json": "0123456789abcdef0123",
}

def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    return hmac.compare_digest(a.encode('utf-8'), b.encode('utf-8'))

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from *filename* and verify that the provided
    *cryptographic_signature* matches the expected signature stored in
    TRUSTED_CONFIG_SIGNATURES.

    Parameters
    ----------
    filename : str
        Name of the configuration file to load.
    cryptographic_signature : str
        Signature that accompanies the configuration data.

    Returns
    -------
    dict or None
        Parsed configuration dictionary if the signature is valid; otherwise,
        ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Retrieve the expected signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(filename)

    # If no signature is known for this file, treat it as invalid
    if expected_signature is None:
        return None

    # Verify the provided signature against the expected one
    if not _constant_time_compare(cryptographic_signature, expected_signature):
        return None

    # Read and parse the configuration file safely
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        # If parsing fails or file read errors occur, treat as invalid
        return None

    # Ensure the parsed data is a dictionary (typical for config files)
    if not isinstance(config_data, dict):
        return None

    return config_data