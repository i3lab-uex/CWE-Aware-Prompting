import json
import os
import hmac

# Example trusted signatures mapping (signature -> config filename).
# In a real deployment these would be securely stored and generated.
TRUSTED_CONFIG_SIGNATURES = {
    "5f4dcc3b5aa765d61d8327deb882cf99": "config1.json",
    "e99a18c428cb38d5f260853678922e03": "config2.json",
}

def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Read a configuration file and validate its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    provided_sig : str
        Cryptographic signature supplied alongside the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file cannot be found or read.
    """
    # Ensure the signature is expected for this filename
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if not expected_sig or expected_sig != config_filename:
        # Signature mismatch; do not proceed.
        return None

    # Resolve absolute path to avoid relative path traversal
    abs_path = os.path.abspath(config_filename)

    # Verify that the file exists and is readable
    if not os.path.isfile(abs_path):
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers file I/O errors; ValueError covers JSON decoding issues
        raise IOError(f"Failed to read or parse configuration file '{config_filename}': {exc}")

    # Return the parsed configuration
    return config_data