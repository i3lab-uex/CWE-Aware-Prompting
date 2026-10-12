import os
import json

# Global mapping of trusted signatures to config file names.
# Example entry: "abcd1234": "config.json"
TRUSTED_CONFIG_SIGNATURES = {
    # Populate with real signatures in production
}

def verify_config_data(config_file: str, provided_signature: str):
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_file : str
        The name (or path) of the configuration file to read.
    provided_signature : str
        The cryptographic signature that accompanies the data.

    Returns
    -------
    dict | None
        Parsed configuration data if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or opened.
    """
    # Ensure the file exists before attempting to read
    if not os.path.isfile(config_file):
        raise IOError(f"Configuration file '{config_file}' not found")

    # Verify that the provided signature matches the trusted one for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_file)
    if expected_sig is None:
        # No trusted signature for this file – treat as untrusted
        return None

    if provided_signature != expected_sig:
        # Signature mismatch – reject the data
        return None

    # Read and parse the configuration file
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            # Assuming JSON format for configuration data
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Treat any I/O or parsing error as a failure to provide valid data
        raise IOError(f"Failed to read or parse configuration file: {exc}") from exc

    return config_data