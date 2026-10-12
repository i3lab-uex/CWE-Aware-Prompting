import json
import os
from hmac import compare_digest

# Global mapping of trusted configuration names to their expected signatures
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "app_settings.json": "a1b2c3d4e5f6...",
    # "db_config.json":   "1234567890abcdef..."
}

def process_config_data(config_name: str, signature: str):
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
    dict or None
        The parsed configuration data if the signature is valid, otherwise ``None``.

    Raises
    ------
    IOError
        If the configuration file cannot be found or read.
    """
    # Resolve absolute path to prevent directory traversal
    config_path = os.path.abspath(config_name)

    if not os.path.isfile(config_path):
        raise IOError(f"Configuration file '{config_name}' not found.")

    # Read the raw data to compute/compare signatures if needed
    try:
        with open(config_path, "rb") as f:
            raw_data = f.read()
    except OSError as exc:
        raise IOError(f"Unable to read configuration file '{config_name}': {exc}") from exc

    # Retrieve the trusted signature for this configuration
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_name)
    if expected_sig is None:
        # No trusted signature registered -> reject
        return None

    # Compare signatures using constant‑time comparison to avoid timing attacks
    if not compare_digest(signature, expected_sig):
        return None

    # Parse JSON safely; any errors propagate as ValueError
    try:
        config_data = json.loads(raw_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Invalid JSON in configuration file '{config_name}': {exc}") from exc

    if not isinstance(config_data, dict):
        # The configuration must be a dictionary
        return None

    return config_data