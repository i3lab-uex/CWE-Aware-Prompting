import json
import os
import hmac

# Example trusted signatures dictionary.
# Keys are filenames and values are the expected cryptographic signatures (hex strings).
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0",
    # Add more entries as needed.
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Hexadecimal signature that accompanies the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist.
    """
    # Verify that the file exists before attempting to read it
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    # Retrieve the expected signature for this file from the trusted list
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if not expected_sig:
        # No trusted signature known for this file: treat as invalid
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(crypt_signature, expected_sig):
        return None

    # Read and parse the configuration file
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, ValueError) as exc:
        # Propagate file read errors or JSON parse errors
        raise IOError(f"Failed to load configuration from '{config_filename}': {exc}") from exc

    return config_data