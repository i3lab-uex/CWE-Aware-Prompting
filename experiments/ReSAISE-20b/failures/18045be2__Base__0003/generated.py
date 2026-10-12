import json
import os
import hmac

# Global mapping of valid signatures (hex strings) to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (replace with real signatures and filenames)
    "a1b2c3d4e5f67890abcdef1234567890": "configA.json",
    "0987654321fedcba0123456789abcdef": "configB.yaml",
}

def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Read a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_file : str
        The name of the configuration file to retrieve.
    provided_signature : str
        The cryptographic signature (hex string) provided with the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration data if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists
    if not os.path.isfile(config_file):
        raise IOError(f"Configuration file '{config_file}' is not available")

    # Verify that the provided signature matches a trusted one for this file
    expected_signature = None
    for sig, fname in TRUSTED_CONFIG_SIGNATURES.items():
        if fname == config_file:
            expected_signature = sig
            break

    # If the file is not in the trusted list, reject it
    if expected_signature is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(provided_signature.lower(), expected_signature.lower()):
        return None

    # Read and parse the configuration file
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            # Assume JSON configuration; adapt if another format is used
            config_data = json.load(f)
    except Exception as e:
        raise IOError(f"Failed to read configuration file '{config_file}': {e}") from e

    return config_data