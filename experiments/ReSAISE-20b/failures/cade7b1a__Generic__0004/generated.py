import json
import os
import hmac

# Global mapping of config file names to their trusted signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries (replace with real values)
    "app_config.json": "f0a1b2c3d4e5f6g7h8i9j0k",
    "db_config.json":  "1234567890abcdef1234",
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load.
    signature : str
        The cryptographic signature that accompanies the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve the full path to the configuration file
    config_path = os.path.abspath(config_name)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_name}' not found at {config_path}")

    # Load the configuration data
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
    except Exception as exc:  # Catch JSON errors and I/O errors
        raise IOError(f"Failed to read configuration file '{config_name}': {exc}") from exc

    # Retrieve the trusted signature for this configuration file
    trusted_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)

    if not trusted_sig:
        # No trusted signature registered for this file
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # Signature verified; return the configuration data
    return config_data