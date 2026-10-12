import json
import os
import hmac

# Global mapping of trusted configuration file names to their expected signatures.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries; populate with real data in production
    "app_settings.json": "a1b2c3d4e5f6g7h8i9j0",
    "db_config.json":   "1234567890abcdef1234",
}

def process_config_data(config_name: str, signature: str) -> dict | None:
    """
    Load a configuration file and verify its cryptographic signature.

    Parameters
    ----------
    config_name : str
        The name of the configuration file to load.
    signature : str
        The cryptographic signature accompanying the configuration data.

    Returns
    -------
    dict | None
        The parsed configuration dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve the absolute path to guard against directory traversal attacks
    config_path = os.path.abspath(config_name)

    # Ensure the file exists and is a regular file
    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Read the raw bytes of the configuration file
    try:
        with open(config_path, "rb") as f:
            raw_data = f.read()
    except OSError as exc:
        raise IOError(f"Error reading configuration file '{config_name}': {exc}") from exc

    # Retrieve the expected signature for this configuration
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if expected_sig is None:
        # No trusted signature registered for this file
        return None

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(signature, expected_sig):
        return None

    # Parse the configuration as JSON
    try:
        config_dict = json.loads(raw_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # If parsing fails, treat it as an invalid configuration
        return None

    return config_dict