import json
import os

# Global dictionary mapping valid cryptographic signatures to their configuration filenames.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries – replace with actual signatures and file names.
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "config.json",
    # Add more signature‑file pairs as needed.
}


def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Retrieve and validate a configuration file using its cryptographic signature.

    Args:
        config_filename: The name of the configuration file to read.
        provided_sig:      The cryptographic signature supplied with the config data.

    Returns:
        A dictionary containing the parsed configuration if the signature is valid.
        None if the signature does not match the trusted value.

    Raises:
        IOError: If the requested configuration file does not exist or cannot be read.
    """
    # Verify that the provided signature is expected for this file.
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None or provided_sig != expected_sig:
        # Signature mismatch – do not proceed.
        return None

    # Ensure the file exists and is readable.
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' not found.")

    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            # Assume the configuration is in JSON format.
            config_data = json.load(f)
    except (OSError, ValueError) as exc:
        # OSError covers file I/O errors; ValueError covers JSON parsing errors.
        raise IOError(f"Failed to read or parse configuration file '{config_filename}': {exc}")

    return config_data