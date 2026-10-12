import os
import json
import hmac

# Global mapping of trusted signatures to configuration file names.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (signature: filename)
    # "sha256$abcd1234...": "config1.json",
}

def evaluate_config_file(config_filename: str, provided_sig: str) -> dict | None:
    """
    Retrieve and validate a configuration file against its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to load.
    provided_sig : str
        Cryptographic signature supplied with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Ensure the file exists before attempting to read it
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' not found")

    # Read the configuration data
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise IOError(f"Failed to read or parse configuration file '{config_filename}': {exc}")

    # Verify that the provided signature is associated with this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if not expected_sig:
        # No trusted signature for this file – reject outright
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(provided_sig, expected_sig):
        return None

    # Signature matches – safe to use the configuration
    return config_data