import json
import os

# Global dictionary mapping configuration file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_config.json": "a1b2c3d4e5f6...",
    # "db_settings.json": "deadbeef12345678",
}

def handle_config_data(file_name: str, file_signature: str):
    """
    Retrieve configuration data from a JSON file and verify its cryptographic signature.

    Parameters
    ----------
    file_name : str
        Name of the configuration file.
    file_signature : str
        Cryptographic signature sent with the configuration data.

    Returns
    -------
    dict or None
        Parsed configuration dictionary if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file does not exist.
    """
    # Verify that the file exists
    if not os.path.isfile(file_name):
        raise IOError(f"Configuration file '{file_name}' does not exist.")

    # Check that we have a trusted signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(file_name)
    if expected_signature is None:
        # No trusted signature known for this file – treat as invalid
        return None

    # Compare the provided signature with the trusted one (case‑insensitive)
    if file_signature.lower() != expected_signature.lower():
        return None

    # Read and parse the JSON configuration
    try:
        with open(file_name, "r", encoding="utf-8") as fp:
            config_data = json.load(fp)
    except (OSError, json.JSONDecodeError):
        # Any read or parse error results in an invalid configuration
        return None

    if not isinstance(config_data, dict):
        # Configuration must be a dictionary
        return None

    return config_data