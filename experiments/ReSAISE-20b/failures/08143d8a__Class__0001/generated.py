import json
import os

# Global dictionary mapping trusted signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries: <signature_hex>: "<config_file_name>"
    "a1b2c3d4e5f6": "app_settings.json",
    # Add real trusted signatures here.
}

def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Reads a configuration file and verifies that the supplied signature matches
    one of the trusted signatures for that file.

    Parameters:
        config_filename (str): Name of the configuration file to load.
        provided_sig (str): Cryptographic signature supplied with the config.

    Returns:
        dict: Parsed configuration data if the signature is valid.
        None: If the signature does not match any trusted entry.

    Raises:
        IOError: If the configuration file cannot be found or read.
    """
    # 1. Check that the provided signature is a known trusted signature for this file.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if not expected_sig or expected_sig != config_filename:
        # Signature mismatch or unknown signature.
        return None

    # 2. Ensure the file exists and is readable.
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist.")

    try:
        with open(config_filename, "r", encoding="utf-8") as fp:
            raw_data = fp.read()
    except OSError as exc:
        raise IOError(f"Failed to read configuration file '{config_filename}': {exc}") from exc

    # 3. Parse the configuration data (assuming JSON for this example).
    try:
        config = json.loads(raw_data)
    except json.JSONDecodeError as exc:
        # The file is present but not valid JSON; treat this as a failure.
        raise IOError(f"Configuration file '{config_filename}' contains invalid JSON: {exc}") from exc

    # 4. Return the parsed configuration.
    return config