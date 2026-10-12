import json
import os
import hmac

# Global dictionary mapping filenames to their trusted signatures
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with real data in production
    "config1.json": "5f4dcc3b5aa765d61d8327deb882cf99",
    "config2.json": "e99a18c428cb38d5f260853678922e03",
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the file containing configuration data.
    crypt_signature : str
        Cryptographic signature sent with the configuration data.

    Returns
    -------
    dict or None
        The parsed configuration dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists before attempting to read
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Retrieve the trusted signature for this file, if any
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_filename)

    # If we have no trusted signature for this file, consider it invalid
    if expected_signature is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_signature, crypt_signature):
        return None

    # Read and parse the configuration file
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # If parsing fails, treat it as an invalid configuration
        return None

    if not isinstance(config_data, dict):
        # Configuration must be a dictionary
        return None

    return config_data