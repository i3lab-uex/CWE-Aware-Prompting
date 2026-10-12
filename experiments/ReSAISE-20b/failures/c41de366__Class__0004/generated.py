import os
import json
import hmac

# Global mapping of filenames to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; replace with actual values.
    "config_prod.json": "a1b2c3d4e5f6g7h8i9j0",
    "config_dev.json":  "1234567890abcdef1234"
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Retrieve the trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # If we have no trusted signature for this file, reject it
        return None

    # Perform a constant‑time comparison to mitigate timing attacks (CWE‑345)
    if not hmac.compare_digest(crypt_signature, expected_sig):
        return None

    # Read and parse the configuration file safely
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        # If the file cannot be parsed or read, treat it as invalid
        return None

    # Return the configuration dictionary
    return config_data