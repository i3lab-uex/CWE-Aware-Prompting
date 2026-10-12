import json
import os
from hmac import compare_digest

# Global dictionary mapping filenames to their expected cryptographic signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (these should be populated with real signatures)
    "app_config.json": "e3b0c44298fc1c149afbf4c8996fb924",
    "db_config.json":  "9f86d081884c7d659a2feaa0c55ad015",
    # Add more trusted filenames and signatures as needed.
}

def retrieve_config_data(config_filename: str, crypt_signature: str) -> dict | None:
    """
    Retrieve configuration data from a file and verify its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        The name of the file containing the configuration data.
    crypt_signature : str
        The cryptographic signature sent with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Retrieve the expected signature for this file from the trusted list
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_signature is None:
        # If we have no trusted signature for this file, treat it as invalid
        return None

    # Verify the provided signature against the expected one using constant‑time comparison
    if not compare_digest(crypt_signature, expected_signature):
        # Signature mismatch – reject the configuration
        return None

    # Read and parse the configuration file (assumed to be JSON)
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        # If the file cannot be read or parsed, propagate the error
        raise IOError(f"Failed to read or parse configuration file '{config_filename}': {exc}") from exc

    # Return the configuration data only if it is a dictionary
    return config_data if isinstance(config_data, dict) else None