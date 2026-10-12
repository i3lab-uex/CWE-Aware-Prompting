import os
import json
import hmac

# Global dictionary mapping filenames to the expected cryptographic signature.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_config.json": "e3b0c44298fc1c149afbf4c8996fb924",
    # "db_config.yaml":  "5d41402abc4b2a76b9719d911017c592",
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from an external file after verifying its
    cryptographic signature.

    Parameters:
        config_filename (str): The name of the configuration file.
        crypt_signature  (str): The signature provided for verification.

    Returns:
        dict | None: Parsed configuration data if the signature is valid;
                     otherwise, None.

    Raises:
        IOError: If the requested configuration file does not exist.
    """
    # Verify that the file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Retrieve the expected signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_filename)

    # If we don't have an expected signature, treat it as invalid
    if expected_signature is None:
        return None

    # Compare signatures using a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(expected_signature, crypt_signature):
        return None

    # Read and parse the configuration file
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            content = f.read()
        # Assume the configuration file is JSON; adjust if a different format is needed
        config_data = json.loads(content)
    except (OSError, ValueError) as e:
        # If the file cannot be read or parsed, return None rather than raising
        return None

    # Ensure the result is a dictionary (common for configuration data)
    if not isinstance(config_data, dict):
        return None

    return config_data