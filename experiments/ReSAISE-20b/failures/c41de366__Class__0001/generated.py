import json
import os
import hmac

# Example trusted signatures dictionary.
# In practice, this should be populated securely and not hard‑coded.
TRUSTED_CONFIG_SIGNATURES = {
    # "config.json": "sha256hashstring",
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Path to the configuration file.
    crypt_signature : str
        Signature provided for the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Retrieve the expected signature from the trusted dictionary
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_filename)

    # If we have no trusted signature for this file, treat it as invalid
    if expected_signature is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypt_signature, expected_signature):
        return None

    # Read and parse the configuration file
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as e:
        # Wrap any exception in IOError for consistency
        raise IOError(f"Failed to read configuration file '{config_filename}': {e}") from e

    # Ensure the parsed data is a dictionary
    if not isinstance(config_data, dict):
        return None

    return config_data