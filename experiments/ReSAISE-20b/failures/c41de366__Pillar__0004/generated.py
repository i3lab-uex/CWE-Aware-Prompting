import json
import os
import hmac

# Global mapping of trusted configuration file names to their expected signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; in practice populate with real values.
    "app_config.json": "3a5f9c2b1e4d6f8a0b7c9e3d5f012345",
    "db_config.json":  "1b2c3d4e5f6a7b8c9d0e1f234567890a",
}

def retrieve_config_data(config_filename: str, crypt_signature: str):
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file to read.
    crypt_signature : str
        Signature supplied with the configuration data.

    Returns
    -------
    dict or None
        Parsed configuration dictionary if the signature matches the trusted value,
        otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file does not exist or cannot be read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(config_filename):
        raise IOError(f"Configuration file '{config_filename}' does not exist")

    # Retrieve the expected signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # No trusted signature available for this file
        return None

    # Use a constant‑time comparison to avoid timing attacks (CWE-693)
    if not hmac.compare_digest(crypt_signature, expected_sig):
        return None

    # Read and parse the configuration file
    try:
        with open(config_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        # Wrap any read/parse errors in an IOError for consistency
        raise IOError(f"Failed to read configuration file '{config_filename}': {e}") from e

    return data