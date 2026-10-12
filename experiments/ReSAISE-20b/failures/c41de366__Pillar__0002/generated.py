import json
import os
import hmac

# Global dictionary mapping config filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries
    "app_config.json": "d41d8cd98f00b204e9800998ecf8427e",
    "db_config.json":  "0cc175b9c0f1b6a831c399e269772661",
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from an external file and verify its cryptographic
    signature against a trusted list.

    Parameters:
        config_filename (str): Name of the configuration file.
        crypt_signature (str): Signature provided with the data.

    Returns:
        dict: Parsed configuration data if signature is valid.
        None: If the signature does not match.

    Raises:
        IOError: If the configuration file does not exist.
    """
    # Ensure the file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Retrieve the expected signature from the trusted dictionary
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)

    # If no trusted signature is known, treat as invalid
    if expected_sig is None:
        return None

    # Use constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(crypt_signature, expected_sig):
        return None

    # Read and parse the configuration file
    with open(config_filename, "r", encoding="utf-8") as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            # Malformed JSON – treat as invalid
            return None

    return config_data