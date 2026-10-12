import json
import os

# Example trusted signatures mapping (signature -> filename)
TRUSTED_CONFIG_SIGNATURES = {
    "abc123def456": "config1.json",
    "789ghi012jkl": "config2.yaml",  # YAML is not parsed in this example
}

def evaluate_config_file(config_filename: str, provided_sig: str):
    """
    Load a configuration file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        The name of the configuration file to retrieve.
    provided_sig : str
        The cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Verify that the provided signature is trusted for this filename
    expected_filename = TRUSTED_CONFIG_SIGNATURES.get(provided_sig)
    if not expected_filename or expected_filename != config_filename:
        # Signature does not match the requested file
        return None

    # Ensure the file exists before attempting to read it
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' is missing.")

    # Read and parse the configuration
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            # Only JSON is supported in this implementation for security reasons.
            content = f.read()
            config_data = json.loads(content)
    except (OSError, ValueError) as exc:
        # OSError covers file I/O errors; ValueError catches JSON parsing errors
        raise IOError(f"Failed to read or parse configuration file '{config_filename}': {exc}") from exc

    # Ensure the parsed data is a dictionary
    if not isinstance(config_data, dict):
        raise IOError(f"Configuration file '{config_filename}' does not contain a JSON object.")

    return config_data