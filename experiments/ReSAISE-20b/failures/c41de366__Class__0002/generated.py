import json
import os
from hmac import compare_digest

# Example trusted signatures mapping. In production, this should be securely stored.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "f1e2d3c4b5a697887766554433221100",
    "db_config.json":  "0123456789abcdef0123456789abcdef",
    # add more trusted config files and their signatures here
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Args:
        config_filename: Name of the configuration file.
        crypt_signature: Signature provided with the configuration data.

    Returns:
        dict: Parsed configuration data if signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        IOError: If the configuration file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # If the file isn't in the trusted list, treat it as untrusted
        return None

    # Compare signatures securely to mitigate timing attacks
    if not compare_digest(crypt_signature, expected_sig):
        # Signature mismatch – do not load the configuration
        return None

    # Read and parse the configuration file safely
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, ValueError) as e:
        # Propagate file read errors or JSON parsing issues
        raise IOError(f"Failed to read or parse configuration: {e}") from e

    return config_data