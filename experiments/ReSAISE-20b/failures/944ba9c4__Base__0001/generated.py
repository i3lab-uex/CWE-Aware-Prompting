import os
import json
import hmac

# Example trusted signatures dictionary.  In production this would be populated securely.
TRUSTED_CONFIG_SIGNATURES = {
    "app_config.json": "5f2e1c4b6d7a8f9e0b1c3d4e5f607182",
    # Add more filename:signature pairs here
}

def validate_config_file(filename: str, cryptographic_signature: str):
    """
    Retrieve configuration data from `filename` and verify that its
    cryptographic signature matches the trusted value.

    Parameters
    ----------
    filename : str
        Path to the configuration file.
    cryptographic_signature : str
        The signature that accompanies the file.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if the signature is valid, otherwise None.

    Raises
    ------
    IOError
        If `filename` does not exist or cannot be read.
    """
    # Ensure the file exists and is readable
    if not os.path.isfile(filename):
        raise IOError(f"Configuration file '{filename}' does not exist.")

    # Load the configuration data (assuming JSON format)
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise IOError(f"Failed to read configuration file '{filename}': {exc}")

    # Retrieve the expected signature for this file
    expected_signature = TRUSTED_CONFIG_SIGNATURES.get(filename)
    if not expected_signature:
        # No trusted signature recorded for this file
        return None

    # Perform a constant‑time comparison to avoid timing attacks (CWE‑347)
    if not hmac.compare_digest(expected_signature, cryptographic_signature):
        return None

    # Signature is valid; return the configuration data
    return config_data