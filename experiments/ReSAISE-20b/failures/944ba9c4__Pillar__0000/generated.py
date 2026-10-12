import os
import json

# Example trusted signatures mapping.
# In a real system this should be securely stored and managed.
TRUSTED_CONFIG_SIGNATURES = {
    "config.yaml": "a1b2c3d4e5f6g7h8i9j0",
    "settings.json": "1234567890abcdef",
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from the specified file and verify its
    cryptographic signature against a trusted list.

    Parameters:
        filename (str): Path to the configuration file.
        cryptographic_signature (str): Signature supplied alongside the config.

    Returns:
        dict: Parsed configuration data if signature is valid.
        None: If the signature does not match.

    Raises:
        IOError: If the file does not exist or cannot be read.
    """
    # Ensure the file exists before attempting to open it
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist")

    # Retrieve the trusted signature for this filename
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(os.path.basename(filename))
    if not expected_signature:
        # No trusted signature known for this file
        return None

    # Verify the supplied signature matches the expected one
    if cryptographic_signature != expected_signature:
        return None

    # At this point the signature is considered valid.
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # Assume JSON configuration; adjust parser if needed
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # If file cannot be read or is not valid JSON, raise IOError
        raise IOError(f"Failed to read or parse configuration file '{filename}': {exc}")

    return config_data